
// Variables
var categorySelected;

// Selectors
var $inputCategory = $("#input-category");
var $inputProduct = $("#input-product");

$inputCategory.change(function(event) {
    categorySelected = $inputCategory.val();
    
    $.ajax({
        url: "/get-products-using-category/" + categorySelected + "/",
        success: function(result) {
            $inputProduct.html("<option selected>Choose...</option>");
            $.each(result, function(index, item) {
                var id = item.id;
                var name = item.name;

                $inputProduct.append("<option value=\"" + id + "\">" + item.name + "</option>");
            });
        }
    });
});
