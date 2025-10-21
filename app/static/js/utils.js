//=====================================================
//  Utility front-end functions
//=====================================================

// Trigger when page loads...
window.onload = (event) => {

    //--------------------------------------------------
    // Prevent duplicate submission of forms
    //--------------------------------------------------
    document.querySelectorAll('form:has(button)').forEach(form => {
        const button = form.querySelector('button');
        form.addEventListener('submit', (e) => {
            if (button.ariaBusy === true) {
                e.preventDefault();
            } else {
                button.ariaBusy = true;
            }
        });
    });

    //--------------------------------------------------
    // Dark/Light Theme Toggle
    //--------------------------------------------------
    const toggleButton = document.getElementById('theme-toggle');
    const html = document.documentElement;

    if (!toggleButton) return; 

 
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        html.setAttribute('data-theme', savedTheme);
    } else {
       
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        html.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }


    toggleButton.textContent = html.getAttribute('data-theme') === 'dark' ? '💡' : '🌑';

   
    toggleButton.addEventListener('click', () => {
        const newTheme = html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        toggleButton.textContent = newTheme === 'dark' ? '💡' : '🌑';
    })
};
