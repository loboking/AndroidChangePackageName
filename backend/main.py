"""
FastAPI 메인 엔드포인트
"""
import os
import re
import tempfile
from pathlib import Path
from typing import Optional
from datetime import datetime

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.processor import AndroidProjectProcessor


app = FastAPI(title="Android Project Rebuilder")

# CORS 설정 (로컬 개발용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_package_name(package_name: str) -> bool:
    """
    Android 패키지명 유효성 검사
    - 최소 2개의 세그먼트 (점으로 구분)
    - 각 세그먼트는 영문 소문자로 시작
    - 영문 소문자, 숫자, 언더스코어만 허용
    """
    pattern = r'^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)+$'
    return bool(re.match(pattern, package_name))


@app.post("/process")
async def process_project(
    project_zip: UploadFile = File(..., description="Android 프로젝트 ZIP 파일"),
    new_package: str = Form(..., description="새 패키지명 (예: com.example.newapp)"),
    new_app_name: str = Form(..., description="새 앱 이름 (예: MyNewApp)"),
    google_services: Optional[UploadFile] = File(None, description="google-services.json (선택)"),
    app_icon: Optional[UploadFile] = File(None, description="앱 아이콘 이미지 (선택)"),
    splash_image: Optional[UploadFile] = File(None, description="스플래시 이미지 (선택)"),
    new_base_url: Optional[str] = Form(None, description="새 BASE_URL (선택)"),
    include_log: bool = Form(True, description="로그 파일 포함 여부")
):
    """
    Android 프로젝트 리빌드 처리

    Returns:
        FileResponse: rebuilt_project.zip
    """
    # 패키지명 유효성 검사
    if not validate_package_name(new_package):
        raise HTTPException(
            status_code=400,
            detail=f"❌ 잘못된 패키지명 형식: '{new_package}'\n\n올바른 형식: com.example.app\n- 영문 소문자로 시작\n- 점(.)으로 최소 2개 이상 구분\n- 영문 소문자, 숫자, 언더스코어(_)만 사용 가능"
        )

    processor = AndroidProjectProcessor()
    temp_files = []

    try:
        # 1. 업로드 파일 임시 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_zip:
            content = await project_zip.read()
            tmp_zip.write(content)
            zip_path = tmp_zip.name
            temp_files.append(zip_path)

        # 2. 선택적 파일 저장
        google_services_path = None
        if google_services:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as tmp_gs:
                content = await google_services.read()
                tmp_gs.write(content)
                google_services_path = tmp_gs.name
                temp_files.append(google_services_path)

        icon_path = None
        if app_icon:
            suffix = Path(app_icon.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_icon:
                content = await app_icon.read()
                tmp_icon.write(content)
                icon_path = tmp_icon.name
                temp_files.append(icon_path)

        splash_path = None
        if splash_image:
            suffix = Path(splash_image.filename).suffix
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_splash:
                content = await splash_image.read()
                tmp_splash.write(content)
                splash_path = tmp_splash.name
                temp_files.append(splash_path)

        # 3. 프로세싱 실행
        result = processor.process(
            zip_path=zip_path,
            new_package=new_package,
            new_app_name=new_app_name,
            google_services_path=google_services_path,
            icon_path=icon_path,
            splash_path=splash_path,
            new_base_url=new_base_url,
            include_log=include_log
        )

        # 4. 결과 반환
        if result['success']:
            output_zip = result['output_zip']

            # ZIP 파일명 생성: package_changed_{앱이름}.zip
            # 한글 파일명은 HTTP 헤더에서 Latin-1 인코딩 에러를 일으키므로 ASCII만 사용
            filename = f"package_changed_{new_app_name}.zip"

            # FileResponse에 filename 직접 전달
            response = FileResponse(
                path=output_zip,
                media_type='application/zip',
                filename=filename
            )

            return response
        else:
            raise HTTPException(
                status_code=500,
                detail={
                    'error': result.get('error', 'Unknown error'),
                    'logs': result['logs']
                }
            )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                'error': str(e),
                'logs': processor.logs
            }
        )

    finally:
        # 임시 파일 정리
        for temp_file in temp_files:
            try:
                if Path(temp_file).exists():
                    os.unlink(temp_file)
            except:
                pass


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "ok", "message": "Android Project Rebuilder is running"}


@app.get("/api/info")
async def info():
    """API 정보"""
    return {
        "name": "Android Project Rebuilder",
        "version": "1.0.0",
        "features": [
            "Package name change",
            "App name change",
            "Version reset (1.0.0)",
            "Firebase config replacement",
            "App icon replacement",
            "Splash image replacement",
            "BASE_URL replacement",
            "Build artifacts cleanup"
        ]
    }


# 프론트엔드 정적 파일 서빙 (반드시 맨 마지막에!)
frontend_path = Path(__file__).parent.parent / "frontend"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")
