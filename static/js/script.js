async function submitForm() {
    const form = document.getElementById('detection-form');
    const loading = document.getElementById('loading');
    const result = document.getElementById('result');
    
    // Show loading indicator
    loading.style.display = 'block';
    result.innerHTML = '';

    // Form data
    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Simulate server response
    const response = await fetch('/detect', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    // Hide loading indicator
    loading.style.display = 'none';

    if (response.ok) {
        const resultData = await response.json();
        result.innerHTML = `<p>detection Result: <strong>${resultData.detection}</strong></p>`;
    } else {
        result.innerHTML = `<p>There was an error processing your request. Please try again.</p>`;
    }
}
