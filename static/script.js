// JavaScript for Python Interpreter Web Interface with Enhanced Features

// Global Variables
let editor;
let executionTimeline = [];
let currentTimelineStep = -1;
let timelineInterval = null;

// DOM Elements
const codeEditorElement = document.getElementById('codeEditor');
const output = document.getElementById('output');
const symbolTable = document.getElementById('symbolTable');
const runBtn = document.getElementById('runBtn');
const clearBtn = document.getElementById('clearBtn');
const tokenizeBtn = document.getElementById('tokenizeBtn');
const astBtn = document.getElementById('astBtn');
const clearOutputBtn = document.getElementById('clearOutputBtn');
const examplesBtn = document.getElementById('examplesBtn');
const examplesMenu = document.getElementById('examplesMenu');
const tokensModal = document.getElementById('tokensModal');
const tokensContent = document.getElementById('tokensContent');
const astModal = document.getElementById('astModal');
const astContent = document.getElementById('astContent');
const loadingSpinner = document.getElementById('loadingSpinner');
const charCount = document.getElementById('charCount');
const lineCount = document.getElementById('lineCount');
const timeline = document.getElementById('timeline');
const timelinePrevBtn = document.getElementById('timelinePrevBtn');
const timelinePlayBtn = document.getElementById('timelinePlayBtn');
const timelineNextBtn = document.getElementById('timelineNextBtn');
const timelineStep = document.getElementById('timelineStep');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    initializeCodeMirror();
    loadExamples();
});

// Initialize CodeMirror
function initializeCodeMirror() {
    editor = CodeMirror.fromTextArea(codeEditorElement, {
        mode: 'javascript',
        theme: 'dracula',
        lineNumbers: true,
        autoCloseBrackets: true,
        matchBrackets: true,
        indentUnit: 4,
        tabSize: 4,
        lineWrapping: true,
        extraKeys: {
            'Ctrl-Enter': executeCode,
            'Cmd-Enter': executeCode,
            'Ctrl-L': clearEditor,
            'Cmd-L': clearEditor
        }
    });
    
    editor.setValue(`// Welcome to the Python Interpreter!
// Try running this example code

let x = 10 + 5;
let y = x * 2;
print(x);
print(y);`);
    
    editor.on('change', () => {
        updateStats();
    });
}

// Event Listeners
runBtn.addEventListener('click', executeCode);
clearBtn.addEventListener('click', clearEditor);
tokenizeBtn.addEventListener('click', showTokens);
astBtn.addEventListener('click', showAST);
clearOutputBtn.addEventListener('click', clearOutput);
examplesBtn.addEventListener('click', toggleExamplesMenu);
timelinePrevBtn.addEventListener('click', previousTimelineStep);
timelinePlayBtn.addEventListener('click', toggleTimelinePlayback);
timelineNextBtn.addEventListener('click', nextTimelineStep);

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to run
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        executeCode();
    }
    // Ctrl/Cmd + L to clear
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
        e.preventDefault();
        clearEditor();
    }
});

// Close dropdown when clicking outside
document.addEventListener('click', (e) => {
    if (!examplesBtn.contains(e.target) && !examplesMenu.contains(e.target)) {
        examplesMenu.classList.remove('show');
    }
});

// Execute Code
async function executeCode() {
    const code = editor.getValue().trim();
    
    if (!code) {
        showError('Please enter some code to execute');
        return;
    }
    
    showLoading(true);
    clearOutput();
    clearTimeline();
    
    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });
        
        const data = await response.json();
        showLoading(false);
        
        if (data.success) {
            displayOutput(data.output);
            displaySymbolTable(data.symbol_table);
            if (data.timeline) {
                displayTimeline(data.timeline);
            }
            showSuccess('Code executed successfully!');
        } else {
            displayError(data.error);
        }
    } catch (error) {
        showLoading(false);
        displayError(`Network error: ${error.message}`);
    }
}

// Show Tokens
async function showTokens() {
    const code = editor.getValue().trim();
    
    if (!code) {
        showError('Please enter some code to tokenize');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/tokenize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });
        
        const data = await response.json();
        showLoading(false);
        
        if (data.success) {
            displayTokens(data.tokens);
            tokensModal.classList.add('show');
        } else {
            showError(data.error);
        }
    } catch (error) {
        showLoading(false);
        showError(`Network error: ${error.message}`);
    }
}

// Show AST
async function showAST() {
    const code = editor.getValue().trim();
    
    if (!code) {
        showError('Please enter some code to parse');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch('/parse', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });
        
        const data = await response.json();
        showLoading(false);
        
        if (data.success) {
            displayAST(data.ast);
            astModal.classList.add('show');
        } else {
            showError(data.error);
        }
    } catch (error) {
        showLoading(false);
        showError(`Network error: ${error.message}`);
    }
}

// Display Output
function displayOutput(outputText) {
    if (!outputText || outputText.trim() === '') {
        output.innerHTML = `
            <div class="output-placeholder">
                <i class="fas fa-check-circle" style="color: var(--success-color);"></i>
                <p>Code executed successfully (no output)</p>
            </div>
        `;
        return;
    }
    
    const lines = outputText.trim().split('\n');
    output.innerHTML = lines.map(line => 
        `<div class="output-line">${escapeHtml(line)}</div>`
    ).join('');
}

// Display Error
function displayError(errorMsg) {
    output.innerHTML = `
        <div class="error-line">
            <i class="fas fa-exclamation-triangle"></i> ${escapeHtml(errorMsg)}
        </div>
    `;
}

// Display Symbol Table
function displaySymbolTable(variables) {
    if (!variables || Object.keys(variables).length === 0) {
        symbolTable.innerHTML = `
            <div class="output-placeholder">
                <i class="fas fa-cube"></i>
                <p>No variables defined</p>
            </div>
        `;
        return;
    }
    
    symbolTable.innerHTML = Object.entries(variables).map(([name, value]) => `
        <div class="variable-item">
            <span class="variable-name">${escapeHtml(name)}</span>
            <span class="variable-value">${escapeHtml(String(value))}</span>
        </div>
    `).join('');
}

// Display Tokens
function displayTokens(tokens) {
    if (!tokens || tokens.length === 0) {
        tokensContent.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No tokens found</p>';
        return;
    }
    
    tokensContent.innerHTML = tokens.map((token, index) => `
        <div class="token-item">
            <span class="token-type">${escapeHtml(token.type)}</span>
            <span class="token-value">${token.value !== null ? escapeHtml(String(token.value)) : '—'}</span>
            <span class="token-position">Line ${token.line}, Col ${token.column}</span>
        </div>
    `).join('');
}

// Load Examples
async function loadExamples() {
    try {
        const response = await fetch('/examples');
        const data = await response.json();
        
        if (data.success) {
            examplesMenu.innerHTML = data.examples.map((example, index) => `
                <div class="example-item" onclick="loadExample(${index})">
                    <div class="example-item-title">${escapeHtml(example.name)}</div>
                </div>
            `).join('');
            
            // Store examples globally
            window.examples = data.examples;
        }
    } catch (error) {
        console.error('Failed to load examples:', error);
    }
}

// Load Example
function loadExample(index) {
    if (window.examples && window.examples[index]) {
        editor.setValue(window.examples[index].code);
        examplesMenu.classList.remove('show');
        clearOutput();
        clearTimeline();
    }
}

// Toggle Examples Menu
function toggleExamplesMenu() {
    examplesMenu.classList.toggle('show');
}

// Close Tokens Modal
function closeTokensModal() {
    tokensModal.classList.remove('show');
}

// Close AST Modal
function closeASTModal() {
    astModal.classList.remove('show');
}

// Clear Editor
function clearEditor() {
    editor.setValue('');
    clearOutput();
    clearTimeline();
}

// Clear Output
function clearOutput() {
    output.innerHTML = `
        <div class="output-placeholder">
            <i class="fas fa-info-circle"></i>
            <p>Click "Run Code" to see output here</p>
        </div>
    `;
    symbolTable.innerHTML = `
        <div class="output-placeholder">
            <i class="fas fa-cube"></i>
            <p>Variables will appear here after execution</p>
        </div>
    `;
}

// Update Stats
function updateStats() {
    const text = editor.getValue();
    const lines = text.split('\n').length;
    const chars = text.length;
    
    charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
    lineCount.textContent = `${lines} line${lines !== 1 ? 's' : ''}`;
}

// Show Loading
function showLoading(show) {
    if (show) {
        loadingSpinner.classList.add('show');
    } else {
        loadingSpinner.classList.remove('show');
    }
}

// Show Success Message
function showSuccess(message) {
    const successDiv = document.createElement('div');
    successDiv.className = 'success-message';
    successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${escapeHtml(message)}`;
    output.insertBefore(successDiv, output.firstChild);
}

// Show Error Message
function showError(message) {
    displayError(message);
}

// Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Display AST
function displayAST(ast) {
    if (!ast) {
        astContent.innerHTML = '<p style="text-align: center; color: var(--text-muted);">No AST data available</p>';
        return;
    }
    
    astContent.innerHTML = '<div class="ast-tree">' + renderASTNode(ast) + '</div>';
}

// Render AST Node recursively
function renderASTNode(node, depth = 0) {
    if (!node || typeof node !== 'object') {
        return '';
    }
    
    const nodeType = node.type || node.__class__ || 'Unknown';
    let html = `<div class="ast-node" style="margin-left: ${depth * 20}px;">`;
    html += `<div class="ast-node-type"><i class="fas fa-sitemap"></i> ${escapeHtml(nodeType)}</div>`;
    html += `<div class="ast-node-details">`;
    
    // Display node properties
    for (const [key, value] of Object.entries(node)) {
        if (key === 'type' || key === '__class__' || key === 'children') continue;
        
        if (Array.isArray(value)) {
            if (value.length > 0 && typeof value[0] === 'object') {
                // Array of nodes
                html += `<div class="ast-node-property"><span class="ast-property-name">${escapeHtml(key)}:</span></div>`;
                html += `<div class="ast-children">`;
                value.forEach(child => {
                    html += renderASTNode(child, depth + 1);
                });
                html += `</div>`;
            } else {
                html += `<div class="ast-node-property"><span class="ast-property-name">${escapeHtml(key)}:</span> <span class="ast-property-value">[${value.map(v => escapeHtml(String(v))).join(', ')}]</span></div>`;
            }
        } else if (value && typeof value === 'object') {
            // Nested object
            html += `<div class="ast-node-property"><span class="ast-property-name">${escapeHtml(key)}:</span></div>`;
            html += `<div class="ast-children">`;
            html += renderASTNode(value, depth + 1);
            html += `</div>`;
        } else if (value !== null && value !== undefined) {
            html += `<div class="ast-node-property"><span class="ast-property-name">${escapeHtml(key)}:</span> <span class="ast-property-value">${escapeHtml(String(value))}</span></div>`;
        }
    }
    
    // Handle children array
    if (node.children && Array.isArray(node.children)) {
        html += `<div class="ast-children">`;
        node.children.forEach(child => {
            html += renderASTNode(child, depth + 1);
        });
        html += `</div>`;
    }
    
    html += `</div></div>`;
    return html;
}

// Display Timeline
function displayTimeline(timelineData) {
    executionTimeline = timelineData;
    currentTimelineStep = -1;
    
    if (!timelineData || timelineData.length === 0) {
        timeline.innerHTML = `
            <div class="output-placeholder">
                <i class="fas fa-history"></i>
                <p>No execution steps recorded</p>
            </div>
        `;
        return;
    }
    
    timeline.innerHTML = timelineData.map((step, index) => {
        let variablesHtml = '';
        if (step.variables && Object.keys(step.variables).length > 0) {
            variablesHtml = `
                <div class="timeline-variables">
                    <strong>Variables:</strong>
                    ${Object.entries(step.variables).map(([name, value]) => `
                        <div class="timeline-variable">
                            <span class="timeline-variable-name">${escapeHtml(name)}:</span>
                            <span class="timeline-variable-value">${escapeHtml(String(value))}</span>
                        </div>
                    `).join('')}
                </div>
            `;
        }
        
        return `
            <div class="timeline-item" data-step="${index}">
                <div class="timeline-step-number">${index + 1}</div>
                <div class="timeline-step-content">
                    <div class="timeline-step-title">${escapeHtml(step.action || 'Step ' + (index + 1))}</div>
                    <div class="timeline-step-description">${escapeHtml(step.description || step.code || '')}</div>
                    ${variablesHtml}
                </div>
            </div>
        `;
    }).join('');
    
    updateTimelineControls();
}

// Clear Timeline
function clearTimeline() {
    executionTimeline = [];
    currentTimelineStep = -1;
    if (timelineInterval) {
        clearInterval(timelineInterval);
        timelineInterval = null;
    }
    timeline.innerHTML = `
        <div class="output-placeholder">
            <i class="fas fa-history"></i>
            <p>Execution steps will appear here</p>
        </div>
    `;
    updateTimelineControls();
}

// Previous Timeline Step
function previousTimelineStep() {
    if (currentTimelineStep > 0) {
        currentTimelineStep--;
        highlightTimelineStep(currentTimelineStep);
    }
}

// Next Timeline Step
function nextTimelineStep() {
    if (currentTimelineStep < executionTimeline.length - 1) {
        currentTimelineStep++;
        highlightTimelineStep(currentTimelineStep);
    }
}

// Toggle Timeline Playback
function toggleTimelinePlayback() {
    if (timelineInterval) {
        // Stop playback
        clearInterval(timelineInterval);
        timelineInterval = null;
        timelinePlayBtn.innerHTML = '<i class="fas fa-play"></i>';
    } else {
        // Start playback
        if (currentTimelineStep >= executionTimeline.length - 1) {
            currentTimelineStep = -1;
        }
        timelinePlayBtn.innerHTML = '<i class="fas fa-pause"></i>';
        timelineInterval = setInterval(() => {
            if (currentTimelineStep < executionTimeline.length - 1) {
                currentTimelineStep++;
                highlightTimelineStep(currentTimelineStep);
            } else {
                clearInterval(timelineInterval);
                timelineInterval = null;
                timelinePlayBtn.innerHTML = '<i class="fas fa-play"></i>';
            }
        }, 1000);
    }
}

// Highlight Timeline Step
function highlightTimelineStep(step) {
    const items = document.querySelectorAll('.timeline-item');
    items.forEach((item, index) => {
        if (index === step) {
            item.classList.add('active');
            item.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            item.classList.remove('active');
        }
    });
    updateTimelineControls();
}

// Update Timeline Controls
function updateTimelineControls() {
    const hasSteps = executionTimeline.length > 0;
    const isAtStart = currentTimelineStep <= 0;
    const isAtEnd = currentTimelineStep >= executionTimeline.length - 1;
    
    timelinePrevBtn.disabled = !hasSteps || isAtStart;
    timelineNextBtn.disabled = !hasSteps || isAtEnd;
    timelinePlayBtn.disabled = !hasSteps;
    
    if (hasSteps) {
        timelineStep.textContent = `Step ${currentTimelineStep + 1} / ${executionTimeline.length}`;
    } else {
        timelineStep.textContent = 'Step 0 / 0';
    }
}

// Close modal when clicking outside
tokensModal.addEventListener('click', (e) => {
    if (e.target === tokensModal) {
        closeTokensModal();
    }
});

astModal.addEventListener('click', (e) => {
    if (e.target === astModal) {
        closeASTModal();
    }
});

console.log('%c🚀 Python Interpreter Web Interface Loaded!', 'color: #00d4ff; font-size: 16px; font-weight: bold;');
console.log('%c✨ Enhanced with Syntax Highlighting, AST Viewer & Execution Timeline!', 'color: #7c3aed; font-size: 14px; font-weight: bold;');
console.log('%cKeyboard Shortcuts:', 'color: #10b981; font-size: 14px; font-weight: bold;');
console.log('  Ctrl/Cmd + Enter: Run Code');
console.log('  Ctrl/Cmd + L: Clear Editor');
