document.addEventListener("DOMContentLoaded", function () {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('show'); // Añadir clase para mostrar
        }, index * 500); // Desfase en el tiempo para cada tarjeta
    });
});
