$(document).ready(function() {
    /*
        jQuery event handlers for toggling the comment editing box.
    */
    // Enable editing
    $(".comment-edit-button").click(function(){
        $(this).closest(".comment").find(".comment-edit-form").toggle()
        $(this).closest(".comment-action").hide()
    })
    // Disable editing
    $(".comment-edit-cancel-button").click(function(){
        $(this).closest(".comment").find(".comment-action").toggle()
        $(this).closest(".comment-edit-form").hide()
    })
});