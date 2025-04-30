// Sidebar Toggle
document.getElementById('sidebarToggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('sidebar-collapsed');
});

// AJAX Content Loading
document.querySelectorAll('[data-ajax]').forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        fetch(this.href, {
            headers: {'X-Requested-With': 'XMLHttpRequest'}
        })
        .then(response => response.text())
        .then(html => {
            document.getElementById('mainContent').innerHTML = html;
            attachFormHandlers();
        });
    });
});

// Form Handling
function attachFormHandlers() {
    console.log('[5] Attaching form submission handlers');
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('mainContent').innerHTML = html;
                attachFormHandlers();
            });
        });
    });
}

// CSRF Token Helper
function getCookie(name) {
    let cookie = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return cookie ? cookie.pop() : '';
}
// Only enable toggle for mobile
function handleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const toggle = document.getElementById('sidebarToggle');
    
    if (window.innerWidth < 992) {
        toggle.addEventListener('click', () => {
            sidebar.classList.toggle('sidebar-collapsed');
        });
    } else {
        sidebar.classList.remove('sidebar-collapsed');
    }
}

// Initial call
handleSidebar();

// Handle window resize
window.addEventListener('resize', handleSidebar);