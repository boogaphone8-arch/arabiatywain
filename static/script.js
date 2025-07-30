// Enhanced interactions for Arabity Wain
document.addEventListener('DOMContentLoaded', function() {
    // Add loading animation to forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '⏳ جاري المعالجة...';
                submitBtn.disabled = true;
            }
        });
    });

    // Add click animations to buttons
    const buttons = document.querySelectorAll('.button, button');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Auto-format phone numbers
    const phoneInputs = document.querySelectorAll('input[name="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.startsWith('249')) {
                value = '+' + value;
            } else if (value.startsWith('0')) {
                value = '+249' + value.substring(1);
            } else if (!value.startsWith('+')) {
                value = '+249' + value;
            }
            e.target.value = value;
        });
    });

    // Add smooth scrolling for anchor links
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });

    // Add typing animation to hero text
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 50);
            }
        };
        setTimeout(typeWriter, 500);
    }

    // Add counter animation to stats
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const finalNumber = parseInt(stat.textContent);
        let currentNumber = 0;
        const increment = finalNumber / 50;
        const timer = setInterval(() => {
            currentNumber += increment;
            if (currentNumber >= finalNumber) {
                stat.textContent = finalNumber;
                clearInterval(timer);
            } else {
                stat.textContent = Math.floor(currentNumber);
            }
        }, 30);
    });

    // Add intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);

    // Observe cards and feature cards
    const animatedElements = document.querySelectorAll('.card, .feature-card, .stat-item');
    animatedElements.forEach(el => {
        observer.observe(el);
    });
});

// Enhanced search functionality
function enhanceSearch() {
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const valueInput = searchForm.querySelector('input[name="value"]');
        const modeSelect = searchForm.querySelector('select[name="mode"]');
        
        valueInput.addEventListener('input', function() {
            const value = this.value.toUpperCase();
            if (value.length > 10 && /^[A-Z0-9]+$/.test(value)) {
                modeSelect.value = 'chassis';
                this.placeholder = 'تم اكتشاف رقم شاسي تلقائياً';
            } else if (value.length <= 10) {
                modeSelect.value = 'plate';
                this.placeholder = 'أدخل رقم اللوحة أو الشاسي';
            }
        });
    }
}

// Initialize enhanced search
enhanceSearch();