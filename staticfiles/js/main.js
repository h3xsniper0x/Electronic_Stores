/**
 * Electronic Store - Main JavaScript
 * Interactive features, form validation, cart updates, and smooth transitions
 */

(function () {
    'use strict';

    // ========================================
    // 1. DOM READY
    // ========================================

    document.addEventListener('DOMContentLoaded', function () {
        initSidebar();
        initFormValidation();
        initCartFunctions();
        initAnimations();
        initQuantityControls();
        initSearchBar();
        initAlertDismiss();
    });

    // ========================================
    // 2. SIDEBAR TOGGLE
    // ========================================

    function initSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const toggleBtn = document.querySelector('.sidebar-toggle');
        const mainWrapper = document.querySelector('.main-wrapper');

        if (toggleBtn && sidebar) {
            toggleBtn.addEventListener('click', function () {
                sidebar.classList.toggle('show');
            });

            // Close sidebar when clicking outside on mobile
            document.addEventListener('click', function (e) {
                if (window.innerWidth < 992) {
                    if (!sidebar.contains(e.target) && !toggleBtn.contains(e.target)) {
                        sidebar.classList.remove('show');
                    }
                }
            });
        }
    }

    // ========================================
    // 3. FORM VALIDATION
    // ========================================

    function initFormValidation() {
        const forms = document.querySelectorAll('form[data-validate]');

        forms.forEach(function (form) {
            form.addEventListener('submit', function (e) {
                if (!validateForm(form)) {
                    e.preventDefault();
                    showNotification('يرجى ملء جميع الحقول المطلوبة', 'error');
                }
            });

            // Real-time validation
            const inputs = form.querySelectorAll('input, textarea, select');
            inputs.forEach(function (input) {
                input.addEventListener('blur', function () {
                    validateField(input);
                });

                input.addEventListener('input', function () {
                    if (input.classList.contains('is-invalid')) {
                        validateField(input);
                    }
                });
            });
        });
    }

    function validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');

        requiredFields.forEach(function (field) {
            if (!validateField(field)) {
                isValid = false;
            }
        });

        return isValid;
    }

    function validateField(field) {
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Required check
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'هذا الحقل مطلوب';
        }

        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                isValid = false;
                errorMessage = 'البريد الإلكتروني غير صالح';
            }
        }

        // Phone validation
        if (field.type === 'tel' && value) {
            const phoneRegex = /^[\d\s\-\+\(\)]{8,}$/;
            if (!phoneRegex.test(value)) {
                isValid = false;
                errorMessage = 'رقم الهاتف غير صالح';
            }
        }

        // Min length
        const minLength = field.getAttribute('minlength');
        if (minLength && value.length < parseInt(minLength)) {
            isValid = false;
            errorMessage = `الحد الأدنى ${minLength} أحرف`;
        }

        // Update UI
        updateFieldValidation(field, isValid, errorMessage);

        return isValid;
    }

    function updateFieldValidation(field, isValid, message) {
        const wrapper = field.closest('.form-group') || field.parentElement;
        let feedback = wrapper.querySelector('.invalid-feedback');

        if (!isValid) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');

            if (feedback) {
                feedback.textContent = message;
            } else {
                feedback = document.createElement('div');
                feedback.className = 'invalid-feedback d-block';
                feedback.textContent = message;
                wrapper.appendChild(feedback);
            }
        } else {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');

            if (feedback) {
                feedback.remove();
            }
        }
    }

    // ========================================
    // 4. CART FUNCTIONS
    // ========================================

    function initCartFunctions() {
        // Add to cart buttons
        const addToCartForms = document.querySelectorAll('.add-to-cart-form');

        addToCartForms.forEach(function (form) {
            form.addEventListener('submit', function (e) {
                const button = form.querySelector('button[type="submit"]');

                // Add loading state
                if (button) {
                    const originalText = button.innerHTML;
                    button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> جاري الإضافة...';
                    button.disabled = true;

                    // Reset after submission (for non-AJAX)
                    setTimeout(function () {
                        button.innerHTML = originalText;
                        button.disabled = false;
                    }, 2000);
                }
            });
        });
    }

    // ========================================
    // 5. QUANTITY CONTROLS
    // ========================================

    function initQuantityControls() {
        document.addEventListener('click', function (e) {
            if (e.target.classList.contains('qty-btn')) {
                const btn = e.target;
                const input = btn.parentElement.querySelector('.qty-input');
                const isPlus = btn.classList.contains('plus');

                let value = parseInt(input.value) || 1;

                if (isPlus) {
                    value++;
                } else {
                    value = Math.max(1, value - 1);
                }

                input.value = value;

                // Trigger change event
                input.dispatchEvent(new Event('change'));
            }
        });
    }

    // ========================================
    // 6. ANIMATIONS
    // ========================================

    function initAnimations() {
        // Intersection Observer for scroll animations
        const observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');

                    // Stagger animation for children
                    const children = entry.target.querySelectorAll('.stagger-item');
                    children.forEach(function (child, index) {
                        child.style.animationDelay = `${index * 0.1}s`;
                        child.classList.add('visible');
                    });
                }
            });
        }, {
            threshold: 0.1,
            rootMargin: '50px'
        });

        // Observe elements with animation classes
        document.querySelectorAll('.animate-on-scroll').forEach(function (el) {
            observer.observe(el);
        });

        // Product cards fade in
        document.querySelectorAll('.product-card').forEach(function (card, index) {
            card.style.animationDelay = `${index * 0.05}s`;
            card.classList.add('animate-fade-in');
        });
    }

    // ========================================
    // 7. SEARCH BAR
    // ========================================

    function initSearchBar() {
        const searchInput = document.querySelector('.search-input');
        let debounceTimer;

        if (searchInput) {
            searchInput.addEventListener('input', function () {
                clearTimeout(debounceTimer);
                debounceTimer = setTimeout(function () {
                    // Could implement live search here
                    console.log('Search:', searchInput.value);
                }, 300);
            });

            // Clear on Escape
            searchInput.addEventListener('keydown', function (e) {
                if (e.key === 'Escape') {
                    searchInput.value = '';
                    searchInput.blur();
                }
            });
        }
    }

    // ========================================
    // 8. ALERT DISMISS
    // ========================================

    function initAlertDismiss() {
        const alerts = document.querySelectorAll('.alert-dismissible');

        alerts.forEach(function (alert) {
            // Auto-dismiss after 5 seconds
            setTimeout(function () {
                fadeOut(alert);
            }, 5000);
        });
    }

    // ========================================
    // 9. UTILITY FUNCTIONS
    // ========================================

    function showNotification(message, type) {
        type = type || 'info';

        const alertClass = {
            'success': 'alert-success',
            'error': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        };

        const notification = document.createElement('div');
        notification.className = `alert ${alertClass[type]} alert-dismissible fade show notification-toast`;
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        // Append to body
        document.body.appendChild(notification);

        // Auto-dismiss
        setTimeout(function () {
            fadeOut(notification);
        }, 4000);
    }

    function fadeOut(element) {
        element.style.transition = 'opacity 0.3s ease';
        element.style.opacity = '0';

        setTimeout(function () {
            element.remove();
        }, 300);
    }

    // ========================================
    // 10. SMOOTH SCROLL
    // ========================================

    document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);

                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ========================================
    // 11. GLOBAL FUNCTIONS (Exposed)
    // ========================================

    // Make functions available globally
    window.toggleSidebar = function () {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.classList.toggle('show');
        }
    };

    window.showNotification = showNotification;

    window.updateQty = function (btn, delta) {
        const input = btn.parentElement.querySelector('.qty-input');
        let val = parseInt(input.value) + delta;
        if (val < 1) val = 1;
        input.value = val;
    };

})();

// ========================================
// 12. CSS INJECTION FOR NOTIFICATIONS
// ========================================

(function () {
    const style = document.createElement('style');
    style.textContent = `
        .notification-toast {
            position: fixed;
            top: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            min-width: 300px;
            max-width: 500px;
            animation: slideDown 0.3s ease;
        }
        
        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
        
        .is-invalid {
            border-color: #dc3545 !important;
        }
        
        .is-valid {
            border-color: #28a745 !important;
        }
    `;
    document.head.appendChild(style);
})();
