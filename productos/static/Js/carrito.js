document.addEventListener('DOMContentLoaded', function() {
    const addToCartButtons = document.querySelectorAll('.añadir_al_carrito');
    const cartItemsContainer = document.querySelector('.cart-items tbody');
    const cartTotalPrice = document.getElementById('cart-total-price');
    const cartToggleButton = document.querySelector('.carrito');
    const cartContainer = document.querySelector('.cart-items-container');
    const cartCloseButton = document.querySelector('.cart-close-button');
    const buyButton = document.getElementById('cart-button-buy');
    const clearButton = document.getElementById('cart-button-clear');

    // Función para agregar un producto al carrito
    function addToCart(producto) {
        let existingCartItem = findCartItem(producto.id);

        if (existingCartItem) {
            // Si el producto ya está en el carrito, incrementa su cantidad
            const quantityElement = existingCartItem.querySelector('.item-quantity');
            quantityElement.value = parseInt(quantityElement.value) + 1;
        } else {
            // Si el producto no está en el carrito, agrégalo con cantidad 1
            const row = createCartItemRow(producto);
            cartItemsContainer.appendChild(row);
        }

        updateTotalPrice();
    }

    // Función para buscar un elemento del carrito por el ID del producto
    function findCartItem(productId) {
        return cartItemsContainer.querySelector(`tr[data-product-id="${productId}"]`);
    }

    // Función para crear una fila de artículo en el carrito
    function createCartItemRow(producto) {
        const row = document.createElement('tr');
        row.dataset.productId = producto.id;
        row.innerHTML = `
            <td><img src="${producto.imagen}" alt="${producto.nombre}" style="width: 50px;"></td>
            <td>${producto.nombre}</td>
            <td>${producto.precio.toFixed(2)}</td>
            <td><input type="number" class="item-quantity" value="1" min="1"></td>
        `;
        return row;
    }

    // Función para actualizar el precio total del carrito
    function updateTotalPrice() {
        let totalPrice = 0;
        cartItemsContainer.querySelectorAll('tr').forEach(row => {
            const price = parseFloat(row.querySelector('td:nth-child(3)').textContent);
            const quantity = parseInt(row.querySelector('.item-quantity').value);
            totalPrice += price * quantity;
        });
        cartTotalPrice.textContent = `Precio total: $${totalPrice.toFixed(2)}`;
    }

    // Función para mostrar u ocultar el carrito
    function toggleCart() {
        cartContainer.classList.toggle('show');
    }

    // Manejar clic en el botón del carrito
    cartToggleButton.addEventListener('click', toggleCart);

    // Manejar clic en el botón de cerrar el carrito
    cartCloseButton.addEventListener('click', toggleCart);

    // Manejar clic en botones de añadir al carrito
    addToCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const productId = event.currentTarget.dataset.productId;
            console.log('Producto ID:', productId);
            const productName = event.currentTarget.closest('.seccion__productos-producto').querySelector('.productos__titulo').textContent;
            const productPrice = parseFloat(event.currentTarget.closest('.seccion__productos-producto').querySelector('.productos__precio').textContent.replace('Precio: ', '').replace('MXN', ''));
            const productImage = event.currentTarget.closest('.seccion__productos-producto').querySelector('.productos__img').src;

            const producto = {
                id: productId,
                nombre: productName,
                precio: productPrice,
                imagen: productImage
            };

            addToCart(producto);
        });
    });

    // Manejar clic en el botón de comprar
    buyButton.addEventListener('click', () => {
        const cartItems = cartItemsContainer.getElementsByTagName('tr');
        if (cartItems.length === 0) {
            Swal.fire({
                title: 'Carrito vacío',
                text: 'El carrito de compras está vacío. Agrega productos antes de realizar la compra.',
                icon: 'error',
                confirmButtonText: 'Aceptar'
            });
            return;
        }

        // Obtener los nombres, cantidades y precios de los productos del carrito
        const productDetails = [];
        const productPrices = [];
        const productQuantities = [];
        for (let i = 0; i < cartItems.length; i++) {
            const productName = cartItems[i].getElementsByTagName('td')[1].textContent;
            const productQuantity = cartItems[i].querySelector('.item-quantity').value;
            const productPrice = parseFloat(cartItems[i].getElementsByTagName('td')[2].textContent.replace(' MXN', ''));
            productDetails.push(encodeURIComponent(productName));
            productQuantities.push(productQuantity);
            productPrices.push(productPrice);
        }

        // Construir la URL con los datos del carrito
        const url = `/comprar_productos/?productos=${productDetails.join(',')}&cantidades=${productQuantities.join(',')}&precio_final=${calculateTotalPrice(productPrices)}`;

        // Mostrar mensaje de confirmación con SweetAlert
        Swal.fire({
            title: '¿Estás seguro de realizar la compra?',
            text: `Resumen del pedido:\n\n${productDetails.map((detail, index) => `${decodeURIComponent(detail)} (Cantidad: ${productQuantities[index]}) - Precio: $${productPrices[index].toFixed(2)} MXN`).join('\n')}\nTotal: $${calculateTotalPrice(productPrices)} MXN\n\nUna vez confirmada la compra, los productos serán enviados y no podrás deshacer esta acción.`,
            icon: 'question',
            showCancelButton: true,
            confirmButtonText: 'Confirmar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                // Redirigir a la página de compra
                window.location.href = url;
            }
        });
    });

    // Función para calcular el precio total
    function calculateTotalPrice(prices) {
        return prices.reduce((total, price) => total + price, 0).toFixed(2);
    }

    // Manejar clic en el botón de vaciar pedido
    clearButton.addEventListener('click', () => {
        // Vaciar el carrito
        cartItemsContainer.innerHTML = '';
        updateTotalPrice();
    });
});