var commentsLevel = 0;

$(document).ready(function() { console.debug("Does this happen twice?"); });

$(document).ready($(".comment-base-link").click(function() {
    var trigger = $(".comment-base-link");
    var commentDivTitle = "[title='" + trigger.attr('title') + "']";
    var insertion_place = $(".comment-div").filter(commentDivTitle);
    var thePostId = -1; // Id no. of the most recent comment on html page
    if (commentsLevel > 0) {
        thePostId = Number.MAX_VALUE;
        var postsList = $('a[title="commentResponseLink"]');
        var length = postsList.length;
        thePostId = parseInt(postsList[length-1].id.substring(2));
    }
    $.ajax({
        url: trigger.attr('title'),
        dataType: "json",
        type: "GET",
        data: {
            "comments_level": commentsLevel.toString(),
            "last_post": thePostId,
        },
        success: function(data, status, jqXHR) {
            if (data.more_comments) {
                trigger.html("Show more comments...");
                commentsLevel++;
            } else {
                trigger.html("No more comments, sorry...");
                trigger.attr("style", "display: none;");
            }
            var s = data.comments_html;
            insertion_place.html(insertion_place.html() + s);
            return;
        }
    });
}));



function scrollTo(jq) {
    $('html, body').animate({
        scrollTop: jq.offset().top
    }, 'fast');
};
