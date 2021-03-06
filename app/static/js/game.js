var config = {
    Role: {
        0: '梅林', 
        1: '派西维尔',
        2: '忠臣',
        3: '刺客',
        4: '莫甘娜',
        5: '莫德雷德',
        6: '奥伯伦',
        7: '爪牙'
    }
}

var info = {
    role: '',
    role_name: 'unknown',
    player_id: '',
    player_num: '',
    known_player: [],

    current_status: 'wait',
    current_round: 0,
    current_try: 0,
    current_team: [],
    mission_player_num: []
}

$(document).ready(function() {
    setTimeout(init, 100);
    $('.action-panel').hide();
    $('#action-panel-grid').show();
});

function init() {
    setTimeout(comet, 10);
    $.get('/game/init', function(data) {
        var content = data['content'];
        for (var i = 0; i < content.length; i += 1) content[i] += 1;
        info.role = data['role'];
        info.role_name = config.Role[data['role']];
        info.player_id = data['player_id'] + 1;
        info.player_num = data['player_num'];
        info.known_player = content
        $('.team-select').map(function() {
            if (parseInt(this.value) >= info.player_num) {
                $(this).parent().remove();
            }
        })
        $('input[name="assassin-select"]').map(function() {
            if (parseInt(this.value) >= info.player_num) {
                $(this).parent().remove();
            }
        })
        dialogNotify('我的身份：' + info.role_name + '\n\n'
            + '我的次序：' + info.player_id + '号\n\n'
            + '看到的玩家：'　+ info.known_player.join('，'));
    });
};

function comet() {
    listening = true;
    $.get('/game/comet', function(data) {
        setTimeout(comet, 1);
        if (data == '') return;
        if (data['type'] == 'message') {
            $('#message-box').append('<div>Player ' + (data['sender'] + 1) + ": " + data['content'] + '</div>');
        } else if (data['type'] == 'player_info') {
            $('#message-box').append('<div>排序: ' + data['content'].join('，') + '</div>');
        } else if (data['type'] == 'register') {
            $('#message-box').append('<div>Player ' + (data['player_id'] + 1) + ": " + data['name'] + ' 已加入。</div>');
        } else if (data['type'] == 'make-team') {
            $('#make-team-panel').show();
            $('#message-box').append('<div>队伍人数: ' + data['num'] + '</div>');
        } else if (data['type'] == 'team-vote') {
            $('#make-team-panel').hide();
            $('#team-vote-panel').show();
            $('#message-box').append('<div>队伍人选: ' + data['content'].map(function(i) { return i + 1; }).join('，') + '。</div>');
        } else if (data['type'] == 'team-result') {
            $('#message-box').append('<div>投票结果: ' + data['content'].map(function(i) { return i == 1 ? '赞同' : '反对'; }).join('，') + '.</div>');
        } else if (data['type'] == 'task-vote') {
            $('#task-vote-panel').show();
        } else if (data['type'] == 'vote') {
            $('#message-box').append('<div>Player ' + (data['player_id'] + 1) + ' 已投票。</div>');
        } else if (data['type'] == 'mission-result') {
            var res = data['result'] ? '成功' : '失败';
            $('#message-box').append('<div>任务' + res + '，' + data['bad_vote_num'] + ' 张失败票。</div>');
        } else if (data['type'] == 'assassin') {
            $('#assassin-panel').slideDown();
        } else if (data['type'] == 'end') {
            var c = (data['result'] == true ? '好人获胜' : '坏人获胜');
            c += data['roles'].map(function(i) { return config.Role[i]; });
            dialogNotify(c);
        } else {
            $('#message-box').append('<div>' + JSON.stringify(data) + '</div>');
        }
    });
}

function add_message(sender, content) {
    $('#message-box').append('');
}

$('#make-team-btn').click(function() {
    $('#make-team-panel').slideUp();
    var content = [];
    $('.team-select:checked').map(function() {
        content.push(parseInt(this.value));
    });
    $.post('/game/action', {
        action: 'make-team',
        content: JSON.stringify({ list: content })
    });
});

$('#team-vote-btn').click(function() {
    $('#team-vote-panel').slideUp();
    vote = $('input[name="team-vote"]:checked').val();
    $.post('/game/action', {
        action: 'team-vote',
        content: vote
    });
});

$('#task-vote-btn').click(function() {
    $('#task-vote-panel').slideUp();
    vote = $('input[name="task-vote"]:checked').val();
    $.post('/game/action', {
        action: 'task-vote',
        content: vote
    });
});

$('#assassin-btn').click(function() {
    $('#assassin-panel').slideUp();
    target = $('input[name="assassin-select"]:checked').val();
    $.post('/game/action', {
        action: 'assasin',
        content: target
    });
});

$('#info').click(function() {
    dialogNotify('我的身份：' + info.role_name + '\n\n'
        + '我的次序：' + info.player_id + '号\n\n'
        + '看到的玩家：'　+ info.known_player.join('，'));
});

$('#send-message').click(function() {
    if ($('#message-content').val() == '') return;
    $.post('/game/action', {
        action: 'message',
        content: $('#message-content').val()
    });
    $('#message-content').val(null);
});

function dialogNotify(content) {
    alert(content);
    // $('.mdl-dialog__content').html(content);
    // $('#show-modal').unbind().avgrund({
    //     width: '280',
    //     height: $('.mdl-dialog').height(),
    //     holderClass: 'mdl-dialog',
    //     onBlurContainer: '.mdl-layout',
    //     template: $('.mdl-dialog').html()
    // }).click();
}

$('#exit').click(function() {
    $.post('/exit', {
        exit: true
    }, function() {
        window.location.href = '/';
    });
});