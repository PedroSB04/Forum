// Função para alternar o menu 
function toggleMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('menuOverlay');
    const body = document.body;

    hamburger.classList.toggle('active');
    mobileMenu.classList.toggle('active');
    overlay.classList.toggle('active');

    if (mobileMenu.classList.contains('active')) {
        body.style.overflow = 'hidden';
        console.log('Menu opened');
    } else {
        body.style.overflow = '';
        console.log('Menu closed');
    }
}

// Função para fechar o menu
function closeMenu() {
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('menuOverlay');
    const body = document.body;

    hamburger.classList.remove('active');
    mobileMenu.classList.remove('active');
    overlay.classList.remove('active');

    body.style.overflow = '';
    
    console.log('Menu closed');
}

// Função para navegação
function navigateTo(page) {
    console.log(`Navigating to: ${page}`);
    
    // Fechar o menu
    closeMenu();
    
    // Simular navegação com feedback visual
    const menuLinks = document.querySelectorAll('.menu-link');
    menuLinks.forEach(link => {
        if (link.textContent.toLowerCase().includes(page)) {
            link.style.background = 'rgba(16, 185, 129, 0.2)';
            link.style.borderLeftColor = '#10b981';
            
            setTimeout(() => {
                link.style.background = '';
                link.style.borderLeftColor = 'transparent';
            }, 1000);
        }
    });
    
    // Aqui você pode adicionar a lógica real de navegação
    switch(page) {
        case 'inicio':
            alert('Redirecionando para a página inicial...');
            break;
        case 'entrar':
            alert('Abrindo página de login...');
            break;
        case 'cadastrar':
            alert('Abrindo página de cadastro...');
            break;
        default:
            console.log('Página não encontrada');
    }
}

// Função para alternar categorias
function toggleCategories() {
    const button = document.querySelector('.select-button');
    
    // Simular dropdown de categorias
    if (button.textContent === 'Todas as Categorias') {
        button.textContent = 'JavaScript';
        setTimeout(() => {
            button.textContent = 'Todas as Categorias';
        }, 2000);
    }
    
    console.log('Categories toggled');
}

// Função para abrir filtros
function openFilter() {
    const filterButton = document.querySelector('.filter-button');
    
    // Animação de clique
    filterButton.style.transform = 'scale(0.95)';
    setTimeout(() => {
        filterButton.style.transform = 'translateY(-1px)';
    }, 100);
    
    // Simular abertura de filtros
    console.log('Filter opened');
}

// Função para juntar-se à comunidade
function joinCommunity() {
    const button = document.querySelector('.join-button');
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
    
    console.log('Joining community');
}

document.addEventListener('DOMContentLoaded', function() {
    // Funcionalidade de busca
    const searchInput = document.getElementById('searchInput');
    
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value;
            
            if (searchTerm.length > 0) {
                console.log('Searching for:', searchTerm);
                
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
});

// Animação de carregamento inicial
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});
