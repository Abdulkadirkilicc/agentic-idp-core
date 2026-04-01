document.addEventListener('DOMContentLoaded', () => {
    // Tab Switching
    const tabBtns = document.querySelectorAll('.tab-btn');
    const views = document.querySelectorAll('.view');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            views.forEach(v => v.classList.remove('active'));
            
            btn.classList.add('active');
            document.getElementById(btn.dataset.target).classList.add('active');
        });
    });

    // Submitting Self-Healing Form
    const healForm = document.getElementById('heal-form');
    healForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btnText = e.target.querySelector('.btn-text');
        const loader = e.target.querySelector('.loader');
        
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');

        const payload = {
            test_name: document.getElementById('fail-name').value,
            error_message: document.getElementById('fail-msg').value,
            traceback: document.getElementById('fail-trace').value,
        };

        try {
            const res = await fetch('/api/v1/analyze-failure', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            
            // Render Result
            const resultDiv = document.getElementById('heal-result');
            resultDiv.style.alignItems = 'flex-start';
            resultDiv.innerHTML = `
                <div class="result-content">
                    <div class="result-card">
                        <span class="tag">Confidence: ${(data.confidence_score * 100).toFixed(0)}%</span>
                        <h3>Reason</h3>
                        <p>${data.failure_reason}</p>
                    </div>
                    <div class="result-card">
                        <h3>Proposed Fix</h3>
                        <p>${data.proposed_fix_description}</p>
                        <div style="margin-top: 1rem;">
                            ${data.patches.map(p => `
                                <div>
                                    <span style="font-size: 0.8rem; color: #9ca3af;">File: ${p.file_path} (${p.action})</span>
                                    <div class="code-block">${escapeHtml(p.new_code_snippet)}</div>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error(error);
            document.getElementById('heal-result').innerHTML = `<p style="color: red;">Platform error occurred.</p>`;
        } finally {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    // Submitting Test Form
    const testForm = document.getElementById('test-form');
    testForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const btnText = e.target.querySelector('.btn-text');
        const loader = e.target.querySelector('.loader');
        
        btnText.classList.add('hidden');
        loader.classList.remove('hidden');

        const payload = {
            endpoint_path: document.getElementById('api-path').value,
            http_method: document.getElementById('api-method').value,
            description: document.getElementById('api-desc').value,
            request_schema: {},
            response_schema: {}
        };

        try {
            const res = await fetch('/api/v1/generate-tests', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await res.json();
            
            // Render Result
            const resultDiv = document.getElementById('test-result');
            resultDiv.style.alignItems = 'flex-start';
            resultDiv.innerHTML = `
                <div class="result-content">
                    <div class="result-card">
                        <span class="tag" style="background: rgba(59, 130, 246, 0.15); color: var(--accent-blue);">Agent Generated Tests</span>
                        <h3>Scenarios Covered</h3>
                        <ul style="margin-bottom: 1rem; color: var(--text-muted); font-size: 0.9rem; padding-left: 1.2rem;">
                            ${data.test_scenarios_covered.map(s => `<li>${s}</li>`).join('')}
                        </ul>
                        <h3>Pytest Code</h3>
                        <div class="code-block">${escapeHtml(data.test_code)}</div>
                    </div>
                </div>
            `;
        } catch (error) {
            console.error(error);
            document.getElementById('test-result').innerHTML = `<p style="color: red;">Platform error occurred.</p>`;
        } finally {
            btnText.classList.remove('hidden');
            loader.classList.add('hidden');
        }
    });

    function escapeHtml(unsafe) {
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
});
