document.addEventListener("DOMContentLoaded", function () {
    const viewDetailButtons = document.querySelectorAll(".view-details");

    viewDetailButtons.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();
            const description = this.getAttribute("data-description");
            const productId = this.getAttribute("data-id");

            if (description === "None" || description === "") {
                // Show the modal if the description is None or empty
                $('#noDescriptionModal').modal('show');
            } else {
                // Navigate to the product details page if there is a description
                window.location.href = `/product/${productId}`;
            }
        });
    });
});
<script>
    $(document).ready(function() {
        $('#query').on('input', function() {
            var query = $(this).val();
            if (query.length > 2) {  // Fetch suggestions for queries longer than 2 characters
                $.ajax({
                    url: '/autocomplete',
                    method: 'GET',
                    data: { q: query },
                    success: function(data) {
                        $('#suggestions').empty();
                        data.forEach(function(item) {
                            $('#suggestions').append(new Option(item, item));
                        });
                    }
                });
            }
        });
    });
</script>
