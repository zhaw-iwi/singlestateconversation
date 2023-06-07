var session = null;
var animate_istyping_interval = null;

function Session(type_id, user_id)  {
    this.type_id = type_id;
    this.user_id = user_id;
}

$(document).ready(function() {
    session = session_from_url();
    get_info();
    get_conversation();
    $("#user_says_input").keypress(function(event) {
        if (event.which === 13) {
            event.preventDefault();
            user_says();
        }
    });
});

function session_from_url() {
    let path = window.location.pathname;
    path_elements = path.split("/");
    return new Session(path_elements[1], path_elements[2]);
}

function reset_conversation_view()  {
    $("#messages").empty();
}

function get_info() {
    $.get("info", function(data) {
        session.name = data.name;
        session.role = data.role;
        session.context = data.context;
        $("#display_type_name").text(session.name);
    });
}

function get_conversation() {
    reset_conversation_view();
    $.get("conversation", function(data) {
        stop_assistant_istyping_temp();
        show_conversation(data);
    });
}

function show_conversation(conversation)    {
    $("#messages").empty();
    $.each(conversation, function(index, current)   {
        let current_message = null;
        if (current.role == "assistant") {
            current_message = get_assistant_message(current.content);
        } else if (current.role == "user")   {
            current_message = get_user_message(current.content);
        }
        if (current_message)    {
            $("#messages").append(current_message);
        }
    });
    $("#user_says_input").prop('disabled', false);
    scroll_down();
}

function scroll_down()   {
    //$('html,body').animate({scrollTop: document.body.scrollHeight / 2}, 'fast');
    //$("section")[0].scrollIntoView({ behavior: "smooth", block: "end", inline: "nearest" });
    $('html,body').animate({scrollTop: document.body.scrollHeight}, 'fast');
}

function show_user_says_incremental(user_says_what)    {
    $('#messages').append(get_user_message(user_says_what));
}

function show_assistant_says_incremental(assistant_says_what)    {
    $('#messages').append(get_assistant_message(assistant_says_what));
}

function start_assistant_istyping_temp()  {
    $('#messages').append(get_assistant_istyping_message());
    animate_istyping_interval = setInterval(function()  {
        animate_istyping()
    }, 700);
    $('html,body').animate({ scrollTop: 9999 }, 'slow');
}  

function stop_assistant_istyping_temp() {
    if (animate_istyping_interval)  {
        clearInterval(animate_istyping_interval);
        animate_istyping_interval = null;
    }
    $(".temporary").remove();
}

function get_assistant_message(content) {
    return $("<div>").addClass("d-flex flex-row justify-content-start mb-4").append(
        $("<i>").addClass("bi bi-emoji-sunglasses").attr("style", "font-size: 2rem;"),
        $("<div>").addClass("p-3 ms-3 border border-secondary").attr("style", "border-radius: 15px;").append(
            $("<p>").addClass("small mb-0").text(content)
        )
    );
}

function get_assistant_istyping_message() {
    return $("<div>").addClass("temporary d-flex flex-row justify-content-start mb-4").append(
        $("<i>").addClass("bi bi-emoji-sunglasses").attr("style", "font-size: 2rem;"),
        $("<div>").addClass("p-3 ms-3 border border-secondary").attr("style", "border-radius: 15px;").append(
            $("<p>").addClass("small mb-0").append(
                $("<i>").addClass("bi bi-chat-dots").attr("id", "istyping_icon")
            )
        )
    );
}

function animate_istyping() {
    if ($("#istyping_icon").hasClass("bi-chat-dots"))    {
        $("#istyping_icon").removeClass("bi-chat-dots");
        $("#istyping_icon").addClass("bi-chat-dots-fill");
    } else  {
        $("#istyping_icon").removeClass("bi-chat-dots-fill");
        $("#istyping_icon").addClass("bi-chat-dots");
    }

}

function get_user_message(content) {
    return $("<div>").addClass("d-flex flex-row justify-content-end mb-4").append(
        $("<div>").addClass("p-3 me-3 border border-secondary").attr("style", "border-radius: 15px;").append(
            $("<p>").addClass("small mb-0").text(content)
        ),
        $("<i>").addClass("bi bi-person-bounding-box").attr("style", "font-size: 2rem;")
    );
}

function user_says()    {
    user_says_what = $("#user_says_input").val();
    if (!user_says_what) {
        return;
    }
    $("#user_says_input").prop('disabled', true);
    $("#user_says_input").val("");
    show_user_says_incremental(user_says_what);
    start_assistant_istyping_temp()
    scroll_down();
    $.ajax({
		type: "POST",
		url: "response_for",
		data: JSON.stringify(user_says_what),
		contentType: "application/json; charset=utf-8",
		dataType: "json",
		success: function(data)	{
            stop_assistant_istyping_temp();
			show_assistant_says_incremental(data.assistant_says);
            $("#user_says_input").prop('disabled', false);
            scroll_down();
		},
		failure: function(errMsg) { alert(errMsg); }
	});
}

function reset(event)    {
    event.preventDefault();
    sure = confirm("Willst Du den bisherigen Chatverlauf löschen?")
    if (sure)   {
        $("#user_says_input").prop('disabled', true);
        $("#user_says_input").val("");
        reset_conversation_view();
        start_assistant_istyping_temp();
        $.ajax({
            type: "DELETE",
            url: "reset",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            success: function(data)	{
                stop_assistant_istyping_temp();
                get_conversation();
            },
            failure: function(errMsg) { alert(errMsg); }
        });
    }
}

function info(event)    {
    event.preventDefault();
    alert("Role\n" + session.role + "\nContext\n" + session.context);
}