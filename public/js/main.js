$(document).ready(function() {
    $(".comment-edit-button").click(function(){
        $(this).closest(".comment").find(".comment-edit-form").toggle()
        $(this).closest(".comment-action").hide()
    })

    $(".comment-edit-cancel-button").click(function(){
        $(this).closest(".comment").find(".comment-action").toggle()
        $(this).closest(".comment-edit-form").hide()
    })
});