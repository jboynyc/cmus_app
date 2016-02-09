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
            padding: 1ex 0;
        }
        @media only screen and (min-width: 768px) and (max-width: 959px) {
            .wrapper { width: 728px; }
        }
        @media only screen and (min-width: 480px) and (max-width: 767px) {
            .wrapper { width: 420px; }
            .controls { font-size: 1.4em; }
        }
        @media only screen and (max-width: 479px) {
            .wrapper { width: 300px; }
            .controls { font-size: 1em; }
        }
        #status {
            overflow: hidden;
            position: relative;
            min-height: 2em;
            padding: 1ex 0;
            background-color: #f5f5f5;
            border: 1px solid #e3e3e3;
            -webkit-border-radius: 1ex;
            -moz-border-radius: 1ex;
            border-radius: 1ex;
            -webkit-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
            -moz-box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
            box-shadow: inset 0 1px 1px rgba(0, 0, 0, 0.05);
        }
        #status p {
            display: inline-block;
            margin: 0 1em;
            line-height: 1em;
            padding: .5em 0 .5em 0;
        }
        .vol {
            position: absolute;
            bottom: 0;
            right: 1ex;
            font-size: .67em;
        }
        #result {
            min-height: 2em;
        }
        footer { position: fixed; bottom: 1ex; }
    </style>
</head>
<body>
<div class="wrapper">

<div id="status"></div>

<div class="controls">

    <span class="btn-group">
        <button class="cmd-btn btn" title="Previous"><i class="icon-fast-backward"></i></button>
        <button class="cmd-btn btn" title="Play"><i class="icon-play"></i></button>
        <button class="cmd-btn btn" title="Stop"><i class="icon-stop"></i></button>
        <button class="cmd-btn btn" title="Next"><i class="icon-fast-forward"></i></button>
    </span>

    <span class="btn-group">
        <button class="cmd-btn btn" title="Mute"><i class="icon-volume-off"></i></button>
        <button class="cmd-btn btn" title="Reduce Volume"><i class="icon-volume-down"></i></button>
        <button class="cmd-btn btn" title="Increase Volume"><i class="icon-volume-up"></i></button>
    </span>

    <button class="status-btn btn btn-round" title="Update Status"><i class="icon-info-sign"></i></button>

</div>

<div id="result"></div>

<footer>
    <p class="small gray-light"><i class="icon-play-circle"></i> This is <code>cmus</code> running on {{host}}.</p>
</footer>

</div>
<script src="/static/zepto.min.js"></script>
<script type="text/javascript">
    function runCommand(command){
        $.ajax({type: 'POST', url: '/cmd', data: {command: command}, context: $("div#result"),
            error: function(){
                var msg = '<p class="red label"><i class="icon-remove"></i> ' + command + '</p>';
                this.html(msg)
            },
            success: function(){
                var msg = '<p class="green label"><i class="icon-ok"></i> ' + command + '</p>'
                this.html(msg)
            }})
    }
    function updateStatus(){
        $.ajax({url: '/status', dataType: 'json', context: $("div#status"), 
            error: function(){
                var msg = '<p class="error">Connection to <code>cmus</code> cannot be established.</p>';
                this.html(msg)
            },
            success: function(response){
                if (response.playing == true) {var msg = '<p>'}
                if (response.playing == false) {var msg = '<p class="gray">'}
                if (response.artist != null & response.title != null & response.album != null & response.date != null)
                    {msg += response.artist + ': <strong>' + response.title + '</strong> (' + response.album + ', ' + response.date.substring(0,4) + ')'}
                else if (response.artist != null & response.title != null & response.album != null)
                    {msg += response.artist + ': <strong>' + response.title + '</strong> (' + response.album + ')'}
                else if (response.artist != null & response.title != null & response.date != null)
                    {msg += response.artist + ': <strong>' + response.title + '</strong> (' + response.date.substring(0,4) + ')'}
                else if (response.artist != null & response.title != null)
                    {msg += response.artist + ': <strong>' + response.title + '</strong>'}
                else if (response.title != null)
                    {msg += '<strong>' + response.title + '</strong>'}
                else if (response.artist != null)
                    {msg += response.artist + ': <strong>(unknown)</strong>'}
                else {msg += '<em>none/unknown</em>'}
                msg += '</p><span class="vol gray">';
                if (response.vol_left != null) {msg += response.vol_left}
                if (response.shuffle == 'true') {msg += ' <i class="icon-random"></i>'}
                if (response.repeat == 'true') {msg += ' <i class="icon-refresh"></i>'}
                msg += '</span>';
                this.html(msg)
            }})
    }
    $(".status-btn").on('click', (function() {
        updateStatus()
    }))
    $(".cmd-btn").on('click', (function(){
        var cmd = $(this).attr('title');
        runCommand(cmd);
        updateStatus();
    }))
    $("div#result").on('click', (function(){
        $(this).empty()
    }))
    Zepto(function() {
        updateStatus()
    })
</script>
</body>
</html>
