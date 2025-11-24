// DOM Elements
const codeEditor = document.getElementById('codeEditor');
const lineNumbers = document.getElementById('lineNumbers');
const output = document.getElementById('output');
const variablesDisplay = document.getElementById('variables');
const runBtn = document.getElementById('runBtn');
const clearBtn = document.getElementById('clearBtn');
const showTokensBtn = document.getElementById('showTokensBtn');
const clearOutputBtn = document.getElementById('clearOutputBtn');
const loadExampleBtn = document.getElementById('loadExampleBtn');
const charCount = document.getElementById('charCount');
const lineCount = document.getElementById('lineCount');

// Modals
const tokensModal = document.getElementById('tokensModal');
const examplesModal = document.getElementById('examplesModal');
const closeModal = document.getElementById('closeModal');
const closeExamplesModal = document.getElementById('closeExamplesModal');
const tokensDisplay = document.getElementById('tokensDisplay');
const examplesDisplay = document.getElementById('examplesDisplay');

// Event Listeners
runBtn.addEventListener('click', runCode);
clearBtn.addEventListener('click', clearEditor);
showTokensBtn.addEventListener('click', showTokens);
clearOutputBtn.addEventListener('click', clearOutput);
loadExampleBtn.addEventListener('click', loadExamples);
closeModal.addEventListener('click', () => tokensModal.style.display = 'none');
closeExamplesModal.addEventListener('click', () => examplesModal.style.display = 'none');

// Close modal when clicking outside
window.addEventListener('click', (e) => {
    if (e.target === tokensModal) {
        tokensModal.style.display = 'none';
    }
    if (e.target === examplesModal) {
        examplesModal.style.display = 'none';
    }
});

// Update line numbers and stats
codeEditor.addEventListener('input', () => {
    updateLineNumbers();
    updateStats();
});

codeEditor.addEventListener('scroll', () => {
    lineNumbers.scrollTop = codeEditor.scrollTop;
});

// Keyboard shortcuts
codeEditor.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + Enter to run
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        runCode();
    }
    
    // Ctrl/Cmd + L to clear
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
        e.preventDefault();
        clearEditor();
    }
    
    // Tab key for indentation
    if (e.key === 'Tab') {
        e.preventDefault();
        const start = codeEditor.selectionStart;
        const end = codeEditor.selectionEnd;
        codeEditor.value = codeEditor.value.substring(0, start) + '    ' + codeEditor.value.substring(end);
        codeEditor.selectionStart = codeEditor.selectionEnd = start + 4;
        updateLineNumbers();
        updateStats();
    }
});

// Functions
function updateLineNumbers() {
    const lines = codeEditor.value.split('\n');
    const lineNumbersText = lines.map((_, i) => i + 1).join('\n');
    lineNumbers.textContent = lineNumbersText;
}

function updateStats() {
    const text = codeEditor.value;
    const lines = text.split('\n').length;
    const chars = text.length;
    
    charCount.textContent = `${chars} character${chars !== 1 ? 's' : ''}`;
    lineCount.textContent = `${lines} line${lines !== 1 ? 's' : ''}`;
}

function clearEditor() {
    codeEditor.value = '';
    updateLineNumbers();
    updateStats();
    addOutputLine('Editor cleared', 'info');
}

function clearOutput() {
    output.innerHTML = '<div class="empty-state"><i class="fas fa-info-circle"></i><p>Click "Run Code" to see output here</p></div>';
}

function addOutputLine(text, type = 'success') {
    // Remove empty state if present
    const emptyState = output.querySelector('.empty-state');
    if (emptyState) {
        output.innerHTML = '';
    }
    
    const line = document.createElement('div');
    line.className = `output-line ${type}`;
    line.textContent = text;
    output.appendChild(line);
    output.scrollTop = output.scrollHeight;
}

async function runCode() {
    const code = codeEditor.value.trim();
    
    if (!code) {
        addOutputLine('Error: No code to execute', 'error');
        return;
    }
    
    // Disable button during execution
    runBtn.disabled = true;
    runBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Running...';
    
    // Clear previous output
    output.innerHTML = '';
    
    try {
        const response = await fetch('/execute', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });
        
        const result = await response.json();
        
        if (result.success) {
            addOutputLine('═══ Execution Started ═══', 'info');
            
            if (result.output && result.output.trim()) {
                const lines = result.output.trim().split('\n');
                lines.forEach(line => {
                    if (line.trim()) {
                        addOutputLine(line, 'success');
                    }
                });
            } else {
                addOutputLine('(No output)', 'info');
            }
            
            addOutputLine('═══ Execution Completed ═══', 'info');
            
            // Update variables display
            updateVariables(result.symbol_table);
        } else {
            addOutputLine('═══ Error ═══', 'error');
            addOutputLine(result.error, 'error');
            
            // Clear variables on error
            variablesDisplay.innerHTML = '<div class="empty-state"><i class="fas fa-cube"></i><p>Variables will appear here after execution</p></div>';
        }
    } catch (error) {
        addOutputLine('═══ Error ═══', 'error');
        addOutputLine(`Network error: ${error.message}`, 'error');
    } finally {
        // Re-enable button
        runBtn.disabled = false;
        runBtn.innerHTML = '<i class="fas fa-play"></i> Run Code';
    }
}

function updateVariables(symbolTable) {
    if (!symbolTable || Object.keys(symbolTable).length === 0) {
        variablesDisplay.innerHTML = '<div class="empty-state"><i class="fas fa-cube"></i><p>No variables defined</p></div>';
        return;
    }
    
    variablesDisplay.innerHTML = '';
    
    for (const [name, value] of Object.entries(symbolTable)) {
        const varItem = document.createElement('div');
        varItem.className = 'variable-item';
        varItem.innerHTML = `
            <span class="variable-name">${name}</span>
            <span class="variable-value">= ${value}</span>
        `;
        variablesDisplay.appendChild(varItem);
    }
}

async function showTokens() {
    const code = codeEditor.value.trim();
    
    if (!code) {
        alert('Please enter some code first');
        return;
    }
    
    try {
        const response = await fetch('/tokenize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code })
        });
        
        const result = await response.json();
        
        if (result.success) {
            tokensDisplay.innerHTML = '';
            
            result.tokens.forEach((token, index) => {
                const tokenItem = document.createElement('div');
                tokenItem.className = 'token-item';
                tokenItem.innerHTML = `
                    <span style="color: #888;">${index + 1}.</span>
                    <span class="token-type">${token.type}</span>
                    ${token.value !== null ? `<span class="token-value">"${token.value}"</span>` : ''}
                    <span class="token-position">(Line ${token.line}, Col ${token.column})</span>
                `;
                tokensDisplay.appendChild(tokenItem);
            });
            
            tokensModal.style.display = 'block';
        } else {
            alert('Error tokenizing code: ' + result.error);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
}

async function loadExamples() {
    try {
        const response = await fetch('/examples');
        const result = await response.json();
        
        if (result.success) {
            examplesDisplay.innerHTML = '';
            
            result.examples.forEach(example => {
                const exampleItem = document.createElement('div');
                exampleItem.className = 'example-item';
                exampleItem.innerHTML = `
                    <div class="example-name">${example.name}</div>
                    <div class="example-preview">${example.code.split('\n').slice(0, 2).join('\n')}...</div>
                `;
                exampleItem.addEventListener('click', () => {
                    codeEditor.value = example.code;
                    updateLineNumbers();
                    updateStats();
                    examplesModal.style.display = 'none';
                    addOutputLine(`Loaded example: ${example.name}`, 'info');
                });
                examplesDisplay.appendChild(exampleItem);
            });
            
            examplesModal.style.display = 'block';
        } else {
            alert('Error loading examples: ' + result.error);
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
}

// Initialize
updateLineNumbers();
updateStats();
addOutputLine('Welcome to the Python Interpreter!', 'info');
addOutputLine('Enter your code and click "Run Code" or press Ctrl+Enter', 'info');
