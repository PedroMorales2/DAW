document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch(this.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Cerrar el modal
            $('#loginModal').modal('hide');
            // Utiliza un breve timeout para asegurar que el modal se cierre antes de redirigir
            setTimeout(() => {
                window.location.href = data.redirect_url; // Asegúrate de que esta URL es la correcta
            }, 500);
        } else {
            // Mostrar mensaje de error proporcionado por el servidor
            document.getElementById('alertContainer').innerHTML = '<div class="alert alert-danger">' + data.message + '</div>';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('alertContainer').innerHTML = '<div class="alert alert-danger">Error al procesar la solicitud.</div>';
    });
});
