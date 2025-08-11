// Função para alternar o menu hambúrguer
function toggleMenu() {
    const hamburger = document.querySelector('.hamburger');
    const spans = hamburger.querySelectorAll('span');
    
    hamburger.classList.toggle('active');
    
    if (hamburger.classList.contains('active')) {
        spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
        spans[1].style.opacity = '0';
        spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
    } else {
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    }
    
    // Simular abertura de menu
    console.log('Menu toggled');
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

// Funcionalidade de busca
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            const searchTerm = e.target.value;
            
            if (searchTerm.length > 0) {
                // Simular busca
                console.log('Searching for:', searchTerm);
                
                // Adicionar efeito visual durante a busca
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
});

// Efeitos de hover melhorados
document.addEventListener('DOMContentLoaded', function() {
    const buttons = document.querySelectorAll('.select-button, .filter-button');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 5px 15px rgba(255, 255, 255, 0.1)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.boxShadow = 'none';
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