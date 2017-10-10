
function make_all_load_content(data) {
    var load_html = '<div class="media">' +
        '<div class="media-body">' +
        '<div class="media-heading">' +
        '<a href="' + data['user_portrait_link'] + '">' +
        '<img class="media-object user-little-portrait pull-left" ' +
        'src="' + data['user_portrait_url'] + '" alt="">' +
        '</a>' +
        '<div class="title-time">' +
        '<a href="' + data['title_link'] + '" class="title-link">' + data['title'] + '</a>' +
        '<h6 class="media-heading">' + data['create_time'] + '</h6>' +
        '</div>' +
        '</div>' +
        '<pre class="my-pre">' + data['body'] + '</pre>' +
        '<div class="btn-group btn-group-justified">' +
        '<a href="' + data['comment_link'] + '" class="btn btn-default btn-no-border">评论 ' +
        '<span id="comment-badge" class="badge">' + data['comment_num'] + '</span></a>' +
        '<a href="' + data['comment_link'] + '" class="btn btn-default btn-no-border">关注 ' +
        '<span id="comment-badge" class="badge">' + data['care_num'] + '</span></a>' +
        '</div>' +
        '</div>' +
        '<hr>' +
        '</div>';

    return load_html;
}

function make_load_content(data) {
    var load_html = '<div class="media">' +
        '<div class="media-body">' +
        '<div class="media-heading">' +
        '<img class="media-object user-little-portrait pull-left" ' +
        'src="' + data['user_portrait_url'] + '" alt="">' +
        '<div class="title-time">' +
        '<a href="' + data['title_link'] + '" class="title-link">' + data['title'] + '</a>' +
        '<h6 class="media-heading">' + data['create_time'] + '</h6>' +
        '</div>' +
        '</div>' +
        '<pre class="my-pre">' + data['body'] + '</pre>' +
        '<div class="btn-group btn-group-justified">' +
        '<a href="' + data['comment_link'] + '" class="btn btn-default btn-no-border">评论 ' +
        '<span id="comment-badge" class="badge">' + data['comment_num'] + '</span></a>' +
        '<a href="' + data['comment_link'] + '" class="btn btn-default btn-no-border">关注 ' +
        '<span id="comment-badge" class="badge">' + data['care_num'] + '</span></a>' +
        '</div>' +
        '</div>' +
        '<hr>' +
        '</div>';

    return load_html;
}

function make_load_comment(data) {
    var load_html = '<div class="media">' +
        '<div class="media-left">' +
        '<a href="' + data['user_portrait_link'] + '">' +
        '<img class="media-object comment-portrait" src="' + data['user_portrait_url'] + '" alt="">' +
        '</a>' +
        '</div>' +
        '<div class="media-body">' +
        '<div class="row">' +
        '<div class="col-xs-8">' +
        '<h4 class="media-heading">' + data['name'] + '</h4>' +
        '</div>' +
        '<div class="col-xs-4 text-right">' +
        '<h6 class="media-heading">' + data['create_time'] + '</h6>' +
        '</div>' +
        '</div>' +
        '<p>' + data['body'] + '</p>' +
        '</div>' +
        '<hr>' +
        '</div>';

    return load_html;
}

// 所在元素开始处加载带用户连接的文章和问答
function load_all_content_prepend($object, data) {
    load_html = make_all_load_content(data);
    $object.prepend(load_html);
}

// 所在元素结尾处加载带用户连接的文章和问答
function load_all_content_append($object, data) {
    load_html = make_all_load_content(data);
    $object.append(load_html);
}

// 开始处用户主页加载文章和问答
function load_content_prepend($object, data) {
    load_html = make_load_content(data);
    $object.prepend(load_html);
}

// 结尾处用户主页加载文章和问答
function load_content_append($object, data) {
    load_html = make_load_content(data);
    $object.append(load_html);
}

// 开始处加载文章和问答的评论
function load_comment_prepend($object, data) {
    load_html = make_load_comment(data);
    $object.prepend(load_html);
}

// 结尾处加载文章和问答的评论
function load_comment_append($object, data) {
    load_html = make_load_comment(data);
    $object.append(load_html);
}

function add_delete_btn() {
    var add_html = '<a class="delete_link" title="删除">' +
        '<span class="glyphicon glyphicon-trash"></span>' +
        '</a>';

    return add_html;
}

function delete_content($object, content) {
    $target = $object.closest('.media');
    article_id = $target.attr('role');
    $.get('/auth/delete_' + content + '/' + article_id + '/', function (data) {
        if (data['status']) {
            $target.slideUp();
            show_message(data);
        }
    });
}