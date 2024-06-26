document.addEventListener('DOMContentLoaded', function() {
    const comprarButtons = document.querySelectorAll('.comprar-button');

    comprarButtons.forEach(button => {
        button.addEventListener('click', () => {
            const productId = button.dataset.productId;
            const productName = button.closest('.seccion__productos-producto').querySelector('.productos__titulo').textContent;
            const productPrice = parseFloat(button.closest('.seccion__productos-producto').querySelector('.productos__precio').textContent.replace('Precio: ', '').replace('MXN', ''));

            // Establecer la cantidad como 1
            const quantity = 1;

            // Construir la URL con los datos del producto y la cantidad
            const url = `/comprar_productos/?productos=${encodeURIComponent(productName)}&precio_final=${productPrice}&cantidades=${quantity}&id=${productId}`;

            swal({
                title: '¿Estás seguro de realizar la compra?',
                text: `Estás a punto de comprar "${productName}" por ${productPrice} MXN.`,
                icon: 'warning',
                buttons: {
                    cancel: 'Cancelar',
                    confirm: 'Comprar'
                },
                dangerMode: true
            }).then((confirmed) => {
                if (confirmed) {
                  window.location.href = url;
                }
            });
        });
    });
});
