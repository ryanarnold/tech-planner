
// Variables
var categorySelected;

// Selectors
var $inputCategory = $("#input-category");
var $inputProduct = $("#input-product");
var $inputStatus = $(".input-status");

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

$inputStatus.change(function(event) {
  var updateStatusPath = "/update-build-product-status/";
  
  var eventTargetId = event.target.id
  var buildProductId = eventTargetId.replace("build-product-", "")
  updateStatusPath += buildProductId + "/";
  
  var newStatus = event.target.value;
  updateStatusPath += newStatus + "/";

  window.location.href = updateStatusPath;
});
