document.addEventListener('DOMContentLoaded', () => {
    const user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!user.username) {
        window.location.href = '/';
        return;
    }

    if (user.role === 'admin') {
        document.querySelector('.admin-only').classList.remove('hidden');
    }

    setupNavigation();
    setupPreviewForm();
    setupAdminPanel();

    document.getElementById('logout-btn').addEventListener('click', () => {
        localStorage.removeItem('user');
        window.location.href = '/';
    });
});

function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-links a');
    const sections = document.querySelectorAll('.dashboard-section');
    
    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            navLinks.forEach(l => l.parentElement.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));
            link.parentElement.classList.add('active');
            const sectionId = link.dataset.section + '-section';
            document.getElementById(sectionId).classList.add('active');
        });
    });
}

function setupPreviewForm() {
    const previewBtn = document.getElementById('preview-btn');
    const templateInput = document.getElementById('template-input');
    const previewDisplay = document.getElementById('preview-display');
    
    previewBtn.addEventListener('click', async () => {
        const template = templateInput.value.trim();
        if (!template) {
            alert('Please enter a template');
            return;
        }
        
        try {
            const response = await fetch('/preview', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ template })
            });
            
            const data = await response.json();
            if (response.ok) {
                previewDisplay.textContent = data.preview;
            } else {
                previewDisplay.textContent = `Error: ${data.error}`;
            }
        } catch (error) {
            console.error('Preview error:', error);
            previewDisplay.textContent = 'Preview failed';
        }
    });
}

function setupAdminPanel() {
    const getFlagButton = document.getElementById('get-flag-btn');
    
    getFlagButton.addEventListener('click', async () => {
        try {
            const response = await fetch('/flag');
            const data = await response.json();
            const flagContainer = document.getElementById('flag-container');
            
            if (response.ok) {
                flagContainer.textContent = data.flag;
                flagContainer.classList.remove('hidden');
            } else {
                alert(data.error);
            }
        } catch (error) {
            console.error('Flag fetch error:', error);
            alert('Failed to fetch flag');
        }
    });
}