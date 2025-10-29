// Standalone PyWebView JavaScript Bridge

let selectedFiles = {
    zip: null,
    googleServices: null,
    appIcon: null,
    splash: null
};

// File selection functions
async function selectZipFile() {
    try {
        const result = await pywebview.api.select_zip_file();
        if (result.success) {
            selectedFiles.zip = result.path;
            document.getElementById('zipFileInfo').textContent = `✓ Selected: ${result.path.split('/').pop()}`;
            document.getElementById('zipFileInfo').style.color = '#27ae60';
        } else {
            alert('No file selected');
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function selectGoogleServicesFile() {
    try {
        const result = await pywebview.api.select_json_file();
        if (result.success) {
            selectedFiles.googleServices = result.path;
            document.getElementById('googleServicesInfo').textContent = `✓ Selected: ${result.path.split('/').pop()}`;
            document.getElementById('googleServicesInfo').style.color = '#27ae60';
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function selectAppIconFile() {
    try {
        const result = await pywebview.api.select_image_file();
        if (result.success) {
            selectedFiles.appIcon = result.path;
            document.getElementById('appIconInfo').textContent = `✓ Selected: ${result.path.split('/').pop()}`;
            document.getElementById('appIconInfo').style.color = '#27ae60';
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function selectSplashFile() {
    try {
        const result = await pywebview.api.select_image_file();
        if (result.success) {
            selectedFiles.splash = result.path;
            document.getElementById('splashInfo').textContent = `✓ Selected: ${result.path.split('/').pop()}`;
            document.getElementById('splashInfo').style.color = '#27ae60';
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

// Form submission
const form = document.getElementById('rebuildForm');
const submitBtn = document.getElementById('submitBtn');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const logContainer = document.getElementById('logContainer');
const successMessage = document.getElementById('successMessage');
const errorMessage = document.getElementById('errorMessage');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Validation
    if (!selectedFiles.zip) {
        alert('Please select a project ZIP file');
        return;
    }

    const newPackage = document.getElementById('newPackage').value;
    const newAppName = document.getElementById('newAppName').value;

    if (!newPackage || !newAppName) {
        alert('Please fill in all required fields');
        return;
    }

    // Initialize UI
    progressContainer.style.display = 'block';
    successMessage.style.display = 'none';
    errorMessage.style.display = 'none';
    logContainer.innerHTML = '';
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Processing...';

    // Progress animation
    progressFill.style.width = '10%';
    addLog('Starting processing...', 'step');

    try {
        // Collect parameters
        const newBaseUrl = document.getElementById('newBaseUrl').value || null;
        const includeLog = document.getElementById('includeLog').checked;

        progressFill.style.width = '30%';
        addLog('Processing project...', 'step');

        // Call Python API
        const result = await pywebview.api.process_project(
            selectedFiles.zip,
            newPackage,
            newAppName,
            selectedFiles.googleServices,
            selectedFiles.appIcon,
            selectedFiles.splash,
            newBaseUrl,
            includeLog
        );

        progressFill.style.width = '70%';

        // Display logs
        if (result.logs && result.logs.length > 0) {
            result.logs.forEach(log => {
                addLog(log, getLogClass(log));
            });
        }

        if (result.success) {
            progressFill.style.width = '90%';
            addLog('Processing completed!', 'success');

            // Prompt for save location
            const newAppNameValue = newAppName.replace(/[^a-zA-Z0-9가-힣]/g, '_');
            const defaultFilename = `package_changed_${newAppNameValue}.zip`;

            const saveResult = await pywebview.api.save_file_dialog(defaultFilename);

            if (saveResult.success) {
                addLog(`Saving to: ${saveResult.path}`, 'step');

                // Copy output file to selected location
                const copyResult = await pywebview.api.copy_file(result.output_zip, saveResult.path);

                if (copyResult.success) {
                    progressFill.style.width = '100%';
                    addLog(`File saved successfully!`, 'success');
                    addLog(copyResult.message, 'success');
                    successMessage.style.display = 'block';
                } else {
                    addLog(`Failed to save file: ${copyResult.error}`, 'error');
                    errorMessage.textContent = `❌ Save Error: ${copyResult.error}`;
                    errorMessage.style.display = 'block';
                }

                // Cleanup
                await pywebview.api.cleanup_processor();
            } else {
                addLog('Save cancelled', 'warning');
                // Still cleanup even if save was cancelled
                await pywebview.api.cleanup_processor();
            }

        } else {
            addLog('Processing failed', 'error');
            errorMessage.textContent = `❌ Error: ${result.error || 'Unknown error'}`;
            errorMessage.style.display = 'block';

            // Cleanup on error
            await pywebview.api.cleanup_processor();
        }

    } catch (error) {
        addLog(`Error: ${error.message}`, 'error');
        errorMessage.textContent = `❌ Error: ${error.message}`;
        errorMessage.style.display = 'block';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = '🚀 Start Project Rebuild';
    }
});

function addLog(message, className = '') {
    const logLine = document.createElement('div');
    logLine.className = `log-line ${className}`;
    logLine.textContent = message;
    logContainer.appendChild(logLine);
    logContainer.scrollTop = logContainer.scrollHeight;
}

function getLogClass(log) {
    if (log.includes('ERROR')) return 'error';
    if (log.includes('WARNING')) return 'warning';
    if (log.includes('---')) return 'step';
    if (log.includes('Successfully') || log.includes('Completed')) return 'success';
    return '';
}

// Help Modal Functions
function toggleHelp() {
    const modal = document.getElementById('helpModal');
    modal.classList.toggle('active');
}

function toggleAccordion(header) {
    const content = header.nextElementSibling;
    const isActive = header.classList.contains('active');

    // Close all accordions
    document.querySelectorAll('.accordion-header').forEach(h => {
        h.classList.remove('active');
        h.nextElementSibling.classList.remove('active');
    });

    // Toggle current accordion
    if (!isActive) {
        header.classList.add('active');
        content.classList.add('active');
    }
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('helpModal');
    if (e.target === modal) {
        modal.classList.remove('active');
    }
});
