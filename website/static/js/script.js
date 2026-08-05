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
    // Busca instantânea apenas no frontend (filtro local)
    const searchInput = document.getElementById('searchInput');
    const postsList = document.querySelector('.posts-list');
    if (searchInput && postsList) {
        searchInput.addEventListener('input', function() {
            const termo = searchInput.value.trim().toLowerCase();
            const postCards = postsList.querySelectorAll('.post-card');
            let algumVisivel = false;
            postCards.forEach(card => {
                const titulo = card.querySelector('.post-title').innerText.toLowerCase();
                const conteudo = card.querySelector('.post-preview').innerText.toLowerCase();
                const usuario = card.querySelector('.author-name').innerText.toLowerCase();
                if (titulo.includes(termo) || conteudo.includes(termo) || usuario.includes(termo)) {
                    card.style.display = '';
                    algumVisivel = true;
                } else {
                    card.style.display = 'none';
                }
            });
            // Mensagem caso nenhum post visível
            let noMsg = postsList.querySelector('.no-posts-message');
            if (!algumVisivel) {
                if (!noMsg) {
                    noMsg = document.createElement('div');
                    noMsg.className = 'no-posts-message';
                    noMsg.innerHTML = '<p>Nenhum post encontrado.</p>';
                    postsList.appendChild(noMsg);
                }
            } else {
                if (noMsg) noMsg.remove();
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

        document.addEventListener('DOMContentLoaded', function() {
            const deleteForms = document.querySelectorAll('.delete-form');
            deleteForms.forEach(form => {
                form.addEventListener('submit', function(event) {
                    const confirmed = confirm('Você tem certeza que deseja excluir esta publicação? A ação não pode ser desfeita.');
                    if (!confirmed) {
                        event.preventDefault(); // Cancela o envio do formulário se o usuário clicar em "Cancelar"
                    }
                });
            });
        });