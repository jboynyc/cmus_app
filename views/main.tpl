<!doctype html>
<html>
<head>
    <title>cmus on {{host}}</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/kube.min.css"/>
    <link rel="stylesheet" type="text/css" href="/static/font-awesome.min.css"/>
    <style type="text/css">
        .wrapper {
            width: 940px;
            margin: 0 auto;
            padding: 2em;
        }
        .controls {
            font-size: 2.2em;
            padding-bottom: 2em;
        }
        @media only screen and (min-width: 768px) and (max-width: 959px) {
            .wrapper { width: 748px; }
        }
        @media only screen and (min-width: 480px) and (max-width: 767px) {
            .wrapper { width: 420px; }
            .controls { font-size: 1.4em; }
        }
        @media only screen and (max-width: 479px) {
            .wrapper { width: 300px; }
            .controls { font-size: 1em; }
        }
        #result {
            min-height: 67%;
        }
    </style>
</head>
<body>
<div class="wrapper">

<div class="controls">

    <span class="btn-group">
        <button class="prev-button btn" title="Previous"><i class="icon-fast-backward"></i></button>
        <button class="play-button btn" title="Play"><i class="icon-play"></i></button>
        <button class="stop-button btn" title="Stop"><i class="icon-stop"></i></button>
        <button class="next-button btn" title="Next"><i class="icon-fast-forward"></i></button>
    </span>

    <span class="btn-group">
        <button class="mute-button btn" title="Mute"><i class="icon-volume-off"></i></button>
        <button class="minus-button btn" title="Reduce Volume"><i class="icon-volume-down"></i></button>
        <button class="plus-button btn" title="Increase Volume"><i class="icon-volume-up"></i></button>
    </span>

    <button class="status-button btn btn-round" title="Show Status"><i class="icon-info-sign"></i></button>

</div>

<div id="result"></div>

<footer>
    <p class="small gray-light"><i class="icon-play-circle"></i> This is <code>cmus</code> running on {{host}}.</p>
</footer>

</div>
<script src="/static/zepto.min.js"></script>
<script type="text/javascript">
    function postCommand(command) {
        $.post('/cmd', {command: command}, function(response){
            $("div#result").html('<pre>'+ response.command + ' ' + response.output + '<pre>')
        }, 'json');
    }
    $(".play-button").on('click', (function() {
        postCommand('player-play');
    }))
    $(".stop-button").on('click', (function() {
        postCommand('player-stop');
    }))
    $(".prev-button").on('click', (function() {
        postCommand('player-prev');
    }))
    $(".next-button").on('click', (function() {
        postCommand('player-next');
    }))
    $(".plus-button").on('click', (function() {
        postCommand('vol +5');
    }))
    $(".minus-button").on('click', (function() {
        postCommand('vol -5');
    }))
    $(".mute-button").on('click', (function() {
        postCommand('vol 0');
    }))
    $(".status-button").on('click', (function() {
        postCommand('status');
    }))
</script>
</body>
</html>
