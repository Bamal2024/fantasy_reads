// Selecciona todas las noticias
const noticias = document.querySelectorAll('.noticia');

// efecto hover adicional
noticias.forEach(noticia => {
    noticia.addEventListener('mouseenter', () => {
        noticia.style.backgroundColor = 'rgba(255, 204, 0, 0.1)';
    });
    noticia.addEventListener('mouseleave', () => {
        noticia.style.backgroundColor = 'rgba(255, 255, 255, 0.05)';
    });
});

// Mensaje al hacer click en "Leer más"
const enlaces = document.querySelectorAll('.noticia a');
enlaces.forEach(enlace => {
    enlace.addEventListener('click', () => {
        console.log('Has hecho click en un enlace de noticia.');
    });
});
