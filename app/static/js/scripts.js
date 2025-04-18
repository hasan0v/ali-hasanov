// Main JavaScript for Ali Hasanov's Website

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips and popovers if Bootstrap is available
    if(typeof bootstrap !== 'undefined') {
        // Initialize tooltips
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
        
        // Initialize popovers
        const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
        const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
    }
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const target = document.querySelector(this.getAttribute('href'));
            if(target) {
                window.scrollTo({
                    top: target.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Auto-hide navigation on scroll down, show on scroll up
    let lastScrollTop = 0;
    const navbar = document.querySelector('header');
    
    if(navbar) {
        window.addEventListener('scroll', function() {
            let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            if(scrollTop > lastScrollTop && scrollTop > 100) {
                // Scroll down
                navbar.style.top = '-100px';
            } else {
                // Scroll up
                navbar.style.top = '0';
            }
            
            lastScrollTop = scrollTop;
        });
    }
    
    // Form validation enhancement
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if(!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Dynamic year for copyright in footer
    const yearEl = document.querySelector('.copyright-year');
    if(yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }
    
    // Handle light/dark theme toggle if implemented
    const themeToggle = document.getElementById('theme-toggle');
    if(themeToggle) {
        themeToggle.addEventListener('click', function() {
            document.body.classList.toggle('dark-theme');
            
            // Save preference to local storage
            const isDarkMode = document.body.classList.contains('dark-theme');
            localStorage.setItem('dark-mode', isDarkMode);
        });
        
        // Check for saved theme preference
        const savedDarkMode = localStorage.getItem('dark-mode') === 'true';
        if(savedDarkMode) {
            document.body.classList.add('dark-theme');
        }
    }
    
    // Animation on scroll for elements with .animate-on-scroll class
    const animatedElements = document.querySelectorAll('.animate-on-scroll');
    
    if(animatedElements.length > 0) {
        // Function to check if element is in viewport
        function isInViewport(element) {
            const rect = element.getBoundingClientRect();
            return (
                rect.top <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.bottom >= 0
            );
        }
        
        // Initial check for elements in viewport
        animatedElements.forEach(el => {
            if(isInViewport(el)) {
                el.classList.add('animated');
            }
        });
        
        // Check on scroll
        window.addEventListener('scroll', () => {
            animatedElements.forEach(el => {
                if(isInViewport(el) && !el.classList.contains('animated')) {
                    el.classList.add('animated');
                }
            });
        });
    }
});
