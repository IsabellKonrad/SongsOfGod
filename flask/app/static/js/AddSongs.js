send_message = function(message='', embed_page='', isnext=false, large=false){
    var m = $('<div />').addClass("modal fade").attr("data-role","dialog");
    var dialog = $('<div />').addClass("modal-dialog");    
    if (large){
        var dialog = $('<div />').addClass("modal-dialog modal-lg");
    }
    var content = $('<div />').addClass("modal-content");
    var body = $('<div />').addClass("modal-body");
    var mtext = $('<p />').text(message);
    var btn_close = $('<button />').addClass("btn btn-default").attr("data-dismiss","modal")
        .css("margin-left","89%").text("Close");
    if (embed_page && !isnext) {
        body.append(btn_close);
        body.append(mtext);
        var embedpage = $('<iframe />').css("border","none").css("width","512")
            .css("height","470").attr("src", embed_page);
        if (large){
            var embedpage = $('<iframe />').css("border","none").css("width","860")
            .css("height","500").attr("src", embed_page);
        }
        body.append(embedpage);
    }
    else if (embed_page && isnext){
        body.append(btn_close);
        body.append(mtext);
        var embedpage = $('<iframe />').css("border","none").css("width","512")
            .css("height","470").attr("src", embed_page);
        body.append(embedpage);
        var btn_next = $('<button />').addClass("btn btn-default")
            .on("click", function() {show_anleitung(embed_page);}).css("margin-right","0")
            .attr("data-dismiss","modal").text("Next");
        body.append(btn_next);
    }
    else {
        body.append(mtext);
        body.append(btn_close);
    }
    content.append(body);
    dialog.append(content);
    m.append(dialog);
    m.modal();
}


show_anleitung = function(embed_page=''){
    if (embed_page){
        if (embed_page == "/anleitungA"){
            send_message("  ","/anleitungB", true);
        }
        if (embed_page == "/anleitungB"){
            send_message("  ","/anleitungC", true);
        }
        if (embed_page == "/anleitungC"){
            send_message("  ","/anleitungCC", true);
        }
        if (embed_page == "/anleitungCC"){
            send_message("  ","/anleitungD", true);
        }
        if (embed_page == "/anleitungD"){
            send_message("  ","/anleitungE", false);
        }

    }
    else {
        send_message("  ", "/anleitungA", true);
    }
}

get_help = function(){
    var songtitle = $("#textarea_songtitle").val();
    var songcontent = $("#textarea_songcontent").val();
    var data = {"songtitle": songtitle, "songcontent": songcontent};
    $.ajax({
        contentType: 'application/json',
        type: 'POST',
        url: 'get_gform_addy',
        data: JSON.stringify(data),
        success: function(d){
            send_message("   ", d.link, false, true)
            //window.open(d.link,'_blank');
        },
        error: function(obj, st, err){
            send_message(err);
        }
    });
}

check_new_song = function(){
  $("#btn_save_song").addClass("hidden");
  $("#btn_mode_2").remove();
  $("#btn_mode_1").remove();
  $("#select_mode").remove();
  $("#show_pdf_check").remove();
  var songtitle = $("#textarea_songtitle").val();
  var songcontent = $("#textarea_songcontent").val();
  var data = {"songtitle": songtitle, "songcontent": songcontent};
  var select_mode = $('<select />').prop("type","radio").css("width", "135px").css("margin-top","3%")
      .addClass("btn btn_mode_suggestion").attr("id","select_mode").css("margin-right","1%")
      .on("change", function() {set_selected_mode(this);});
  var option = $('<option />').val("").text("andere Tonart").attr("disabled", "disabled");
  select_mode.append(option);
  var modes_vec = ["As","f","Es","c","B","g","F","d","C","a","G","e","D","h","A","fis","E","cis"];
  modes_vec.forEach(function(element){
      var option = $('<option />').text(element).val(element);
      select_mode.append(option);});
  select_mode.prop('selectedIndex', 0) 
    $.ajax({
    contentType: 'application/json',
    type: 'POST',
    url: 'checksong',
    data: JSON.stringify(data),
    success: function(d){
        if (d.chords_success == false){
            send_message("Something is wrong with your chords.")
        }
        else if (d.latex_success == 0){
          send_message("Something is wrong with your song content.")
        }
        else if (d.mode_success == false){
            send_message("Something is wrong with your chords.")
        }
        else {
          $("#show_pdf_check_placeholder").append(d.path);
          var mode1 = d.mode1;
          var mode2 = d.mode2;
          var btn_mode_1 = $('<button />').prop("type","radio").attr("id","btn_mode_1").text(mode1)
            .addClass("btn btn_mode_suggestion").val(mode1).css("margin-top","3%")
            .css("margin-right","1%").on("click", function() {set_selected_mode(this);});
          var btn_mode_2 = $('<button />').prop("type","radio").attr("id","btn_mode_2").text(mode2)
            .addClass("btn btn_mode_suggestion").css("margin-right","1%").css("margin-top","3%")
            .val(mode2).on("click", function() {set_selected_mode(this);});
          $("#btn_modes_placeholder").append(btn_mode_1);
          $("#btn_modes_placeholder").append(btn_mode_2);
          $("#btn_modes_placeholder").append(select_mode);
          $("#btn_modes_placeholder").removeClass("hidden");
      }
    },
    error: function(obj, st, err){
      alert(err);
    }
  });
}


set_selected_mode = function(e) {
  $("#btn_save_song").removeClass("hidden");
  if (!$(e).hasClass('active')){
    $(e).addClass('active');
    $(e).siblings().removeClass('active');
    $(e).siblings().prop('selectedIndex', 0);
  }
}


save_song = function(){
    var mode=0;
    if ($("#btn_mode_1").hasClass('active')){
        var mode = $("#btn_mode_1").val();
    }
    else if ($("#btn_mode_2").hasClass('active')){
        var mode = $("#btn_mode_2").val();
    }
    else if ($("#select_mode").hasClass('active')){
        var mode = $("#select_mode").find(":selected").val();
    }
    else {
        send_message("Choose a mode to continue.")
    }
    var songtitle = $("#textarea_songtitle").val();
    if (mode != 0){
       var data = {"mode": mode, "songtitle": songtitle};
       $.ajax({
          contentType: 'application/json',
          type: 'POST',
          url: 'savesong',
          data: JSON.stringify(data),
          success: function(d){
            if (d.success){
              send_message("Lied erfolgreich gespeichert.");
            }
            else {
              send_message("Wähle einen anderen Liedtitel. Diesen gibt es schon.");
            }
          },
          error: function(obj, st, err){
            send_message(err);
          }
       });
    }
}

$( document ).ready(function() {
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
    (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
    m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-73396169-1', 'auto');
  ga('send', 'pageview');
});