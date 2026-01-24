const API_URL = window.location.origin;

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const predictBtn = document.getElementById('predictBtn');
    const btnText = predictBtn.querySelector('.btn-text');
    const btnIcon = predictBtn.querySelector('i');
    const loader = document.getElementById('btnLoader');
    const resultSection = document.getElementById('resultSection');
    const resetBtn = document.getElementById('resetBtn');
    const apiStatus = document.getElementById('apiStatus');
    const statusDot = document.querySelector('.status-dot');

    // Check API Health
    checkHealth();

    // Validation Logic
    const inputs = form.querySelectorAll('input, select');
    const validateField = (field, showErrors = true) => {
        const errorSpan = document.getElementById(`${field.id}_error`);
        if (!errorSpan) return true;

        let isValid = true;
        let message = '';

        if (field.required && (!field.value || field.value === '')) {
            isValid = false;
            message = 'This field is required';
        } else if (field.type === 'number') {
            const val = parseFloat(field.value);
            const min = parseFloat(field.getAttribute('min'));
            const max = parseFloat(field.getAttribute('max'));
            if (!isNaN(min) && val < min) {
                isValid = false;
                message = `Value must be at least ${min}`;
            } else if (!isNaN(max) && val > max) {
                isValid = false;
                message = `Value must be at most ${max}`;
            }
        }

        const isTouched = field.dataset.touched === 'true';
        if (showErrors && isTouched) {
            errorSpan.textContent = isValid ? '' : message;
            field.style.borderColor = isValid ? '' : '#dc2626';
        }
        return isValid;
    };

    const validateForm = (showErrors = true) => {
        let isFormValid = true;
        inputs.forEach(input => {
            if (!validateField(input, showErrors)) {
                isFormValid = false;
            }
        });
        predictBtn.disabled = !isFormValid;
        return isFormValid;
    };

    // Initial validation (silent)
    validateForm(false);

    // Add listeners for real-time validation
    inputs.forEach(input => {
        input.dataset.touched = 'false';

        input.addEventListener('input', () => {
            input.dataset.touched = 'true';
            validateForm(true);
        });

        input.addEventListener('change', () => {
            input.dataset.touched = 'true';
            validateForm(true);
        });

        input.addEventListener('blur', () => {
            input.dataset.touched = 'true';
            validateField(input, true);
        });
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!validateForm()) return;

        // Show loading state
        setLoading(true);

        // Gather form data
        const formData = new FormData(form);
        const data = {};

        // Convert FormData to JSON object with correct types
        for (let [key, value] of formData.entries()) {
            // Convert numbers and enums to integers
            if (value !== '') {
                data[key] = parseFloat(value);
            }
        }

        try {
            const response = await fetch(`${API_URL}/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error('Prediction failed');
            }

            const result = await response.json();
            displayResult(result, response.headers.get('X-Process-Time'));

        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your request. Please ensure the API is running.');
        } finally {
            setLoading(false);
        }
    });

    resetBtn.addEventListener('click', () => {
        resultSection.classList.add('hidden');
        form.reset();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    async function checkHealth() {
        try {
            const response = await fetch(`${API_URL}/health`);
            if (response.ok) {
                apiStatus.textContent = "System Online";
                statusDot.style.backgroundColor = "var(--success-color)";
                statusDot.style.boxShadow = "0 0 10px var(--success-color)";
            } else {
                throw new Error('API Unhealthy');
            }
        } catch (error) {
            apiStatus.textContent = "System Offline";
            statusDot.style.backgroundColor = "var(--danger-color)";
            statusDot.style.boxShadow = "0 0 10px var(--danger-color)";
        }
    }

    function setLoading(isLoading) {
        predictBtn.disabled = isLoading;
        if (isLoading) {
            btnText.textContent = 'Analyzing...';
            btnIcon.style.display = 'none';
            loader.style.display = 'block';
        } else {
            btnText.textContent = 'Analyze Risk';
            btnIcon.style.display = 'inline-block';
            loader.style.display = 'none';
        }
    }

    function displayResult(result, latency) {
        // Update UI elements
        const riskScore = Math.round(result.churn_probability * 100);
        const riskCircle = document.getElementById('riskCircle');
        const riskLabel = document.getElementById('riskLabel');
        const predictionText = document.getElementById('predictionText');
        const confidenceText = document.getElementById('confidenceText');
        const latencyText = document.getElementById('latencyText');
        const recommendation = document.querySelector('.action-recommendation');
        const recText = document.getElementById('recommendationText');
        const recTitle = recommendation.querySelector('h3');

        // Update values
        document.getElementById('riskScore').textContent = `${riskScore}%`;
        riskLabel.textContent = `${result.risk_level} Risk`;
        predictionText.textContent = result.churn_prediction === 1 ? 'Churn Likely' : 'Retention Likely';
        confidenceText.textContent = `${(result.confidence * 100).toFixed(1)}%`;

        if (latency) {
            latencyText.textContent = `${(parseFloat(latency) * 1000).toFixed(0)}ms`;
        }

        // Style based on risk
        let color, bg;
        if (result.risk_level === 'High') {
            color = 'var(--danger-color)';
            bg = 'rgba(239, 68, 68, 0.1)';
            recText.textContent = "Immediate intervention required! Offer a discount or loyalty bonus immediately.";
            recTitle.style.color = color;
            recommendation.style.borderColor = 'rgba(239, 68, 68, 0.2)';
        } else if (result.risk_level === 'Medium') {
            color = 'var(--warning-color)';
            bg = 'rgba(245, 158, 11, 0.1)';
            recText.textContent = "Monitor usage patterns. Consider sending a satisfaction survey.";
            recTitle.style.color = color;
            recommendation.style.borderColor = 'rgba(245, 158, 11, 0.2)';
        } else {
            color = 'var(--success-color)';
            bg = 'rgba(16, 185, 129, 0.1)';
            recText.textContent = "Customer is satisfied. No immediate action required.";
            recTitle.style.color = color;
            recommendation.style.borderColor = 'rgba(16, 185, 129, 0.2)';
        }

        riskCircle.style.background = `conic-gradient(${color} ${riskScore}%, transparent 0%)`;
        riskLabel.style.color = color;
        recommendation.style.background = bg;

        // Show result
        resultSection.classList.remove('hidden');
        resultSection.scrollIntoView({ behavior: 'smooth' });
    }
});
