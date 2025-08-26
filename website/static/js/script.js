// Função para alternar o menu 
function toggleMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('menuOverlay');
    const body = document.body;

    if (hamburger && mobileMenu && overlay) {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        overlay.classList.toggle('active');

        if (mobileMenu.classList.contains('active')) {
            body.style.overflow = 'hidden';
        } else {
            body.style.overflow = '';
        }
    }
}

// Função para fechar o menu
function closeMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('menuOverlay');
    const body = document.body;

    if (hamburger && mobileMenu && overlay) {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        overlay.classList.remove('active');
        body.style.overflow = '';
    }
}

// Função para alternar categorias
function toggleCategories() {
    const button = document.querySelector('.select-button');
    
    if (button) {
        // Simular dropdown de categorias
        if (button.textContent === 'Todas as Categorias') {
            button.textContent = 'JavaScript';
            setTimeout(() => {
                button.textContent = 'Todas as Categorias';
            }, 2000);
        }
    }
}

// Função para abrir filtros
function openFilter() {
    const filterButton = document.querySelector('.filter-button');
    
    if (filterButton) {
        // Animação de clique
        filterButton.style.transform = 'scale(0.95)';
        setTimeout(() => {
            filterButton.style.transform = 'translateY(-1px)';
        }, 100);
    }
}

// Função para juntar-se à comunidade
function joinCommunity() {
    const button = document.querySelector('.join-button');
    
    if (button) {
        const originalText = button.textContent;
        
        button.textContent = 'Juntando-se...';
        button.style.transform = 'scale(0.98)';
        
        setTimeout(() => {
            button.textContent = '✅ Bem-vindo à comunidade!';
            button.style.background = 'linear-gradient(135deg, #10b981, #059669)';
            
            setTimeout(() => {
                button.textContent = originalText;
                button.style.background = 'linear-gradient(135deg, #6366f1, #8b5cf6)';
                button.style.transform = 'translateY(-2px)';
            }, 3000);
        }, 1500);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidade de busca
    const searchInput = document.getElementById('searchInput');
    
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value;
            
            if (searchTerm.length > 0) {
                const emptyState = document.querySelector('.empty-state');
                if (emptyState) {
                    emptyState.style.opacity = '0.5';
                    
                    setTimeout(() => {
                        emptyState.style.opacity = '1';
                    }, 500);
                }
            }
        });
    }

    // Efeitos de hover melhorados
    const buttons = document.querySelectorAll('.select-button, .filter-button');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 5px 15px rgba(255, 255, 255, 0.1)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'none';
        });
    });

    // Fechar menu ao pressionar ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const mobileMenu = document.getElementById('mobileMenu');
            if (mobileMenu && mobileMenu.classList.contains('active')) {
                closeMenu();
            }
        }
    });

    // Fechar menu ao redimensionar a tela
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeMenu();
        }
    });

    // VALIDAÇÃO DO FORMULÁRIO DE CADASTRO
    const signupForm = document.getElementById('signupForm');
    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirmPassword').value;
            const email = document.getElementById('email').value;
            const username = document.getElementById('username').value;
            
            // Validações
            if (username.length < 3) {
                alert('O nome de usuário deve ter pelo menos 3 caracteres');
                return;
            }
            
            if (!email.includes('@') || !email.includes('.')) {
                alert('Por favor, insira um email válido');
                return;
            }
            
            if (password.length < 8) {
                alert('A senha deve ter pelo menos 8 caracteres');
                return;
            }
            
            if (password !== confirmPassword) {
                alert('As senhas não coincidem');
                return;
            }
            
            // Simulação de sucesso
            alert('Conta criada com sucesso! Redirecionando para login...');
            // Redirecionar para página de login
            window.location.href = '/login';
        });
    }

    // VALIDAÇÃO DO FORMULÁRIO DE LOGIN
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            // e.preventDefault(); // <-- Comentado para permitir o envio real ao backend Flask
            
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            
            // Validações básicas
            if (!email || !password) {
                alert('Por favor, preencha todos os campos');
                e.preventDefault(); // <-- Só impede se houver erro
                return;
            }
            
            if (!email.includes('@') || !email.includes('.')) {
                alert('Por favor, insira um email válido');
                e.preventDefault(); // <-- Só impede se houver erro
                return;
            }
            
            // Simulação de login bem-sucedido
            // alert('Login realizado com sucesso! Redirecionando...');
            // window.location.href = '/';
            // <-- Comentado para não redirecionar via JS, deixando o backend Flask cuidar disso
        });
    }

    document.querySelector('.login-button').addEventListener('click', function() {
        document.getElementById('loginForm').submit();
    });
});

    // Adiciona feedback visual aos campos
    // Feedback visual básico para formulários (apenas UX)
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.style.borderColor = '#6366f1';
        });
        
        input.addEventListener('blur', function() {
            if (this.value.trim()) {
                this.style.borderColor = '#10b981';
            } else {
                this.style.borderColor = '';
            }
        });
    });

    // Animação visual para botões de submit
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });
});

// Animação de carregamento inicial
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});