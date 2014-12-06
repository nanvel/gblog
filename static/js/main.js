(function($, undefined) {
	$(window).resize(function(){
		sideBarFix();
	})
	$(window).scroll(function(){
		sideBarFix();
	})

	function sideBarFix(){
		"use strict";
		var SelectHeight;
		if($('.left_sidebar_content_area').height()>=$('.main_content_area').height()){
			SelectHeight = $('.left_sidebar_content_area').height();
			SelectHeight += "px"; 
			$('.left_sidebar_content_area, .main_content_area').css({'min-height':SelectHeight});
		}
		else{
			SelectHeight = $('.main_content_area').height();
			SelectHeight += "px"; 
			$('.left_sidebar_content_area, .main_content_area').css({'min-height':SelectHeight});
		}
	}

	function loadPage(a, b, l){
		"use strict";
		$.ajax({
		    url: '/post',
		    dataType: 'json',
		 	data: {a: a, b: b, l: l},
		 	type: 'GET',
		    success: function (data) {
		    	$('.js-post').remove();
		    	for (var i=data.posts.length - 1; i >= 0 ; i--) {
		    		$('.js-posts').prepend(data.posts[i].content);
		    	}
		        if (a || b){
		        	var stateObj = {a: a, b: b, l: l};
		        	var h = [];
		        	if(a){
		        		h.push('a=' + a)
		        	}
		        	if(b){
		        		h.push('b=' + b)
		        	}
		        	if(l) {
		        		h.push('l=' + l);
		        	}
					history.pushState(stateObj, 'Posts starting from ' + a || b, '#' + h.join('&'));
		        } else {
		        	history.pushState(stateObj, 'Home', '#');
		        }
		    },
		    beforeSend: function(){
				$('.js-button-forvard').attr('disabled', true);
				$('.js-button-back').attr('disabled', true);
				$('.js-button-latest').attr('disabled', true);
		    },
		    error: function(){
		    },
		    complete: function(){
		    	$('.js-button-forvard').attr('disabled', false);
		    	$('.js-button-back').attr('disabled', false);
		    	$('.js-button-latest').attr('disabled', false);
		    }
		});
	}

	function getHashParams(){
		var page_params = window.location.hash.split('#');
		var params = {};
		if(page_params.length == 2){
			page_params = page_params[1];
			page_params = page_params.split('&');
			for (var i=0; i<page_params.length; i++) {
                var parts = page_params[i].split('=');
                if(parts.length == 2){
                	params[parts[0]] = parts[1];
                }
            }
		}
		return params;
	}

	$(document).ready(function(){
		var params = getHashParams()
		loadPage(params.a, params.b, params.l);
		sideBarFix();
		$('.nav a').click(function(){
			if($(this).next().is('ul')){
				if($(this).hasClass('open')){
					$(this).next('ul').slideUp(200);
					$(this).removeClass('open');
				}
				else{
					$(this).next('ul').slideDown(200);
					$(this).addClass('open');
				}
				
				return false;
			}
			else{
				return true;
			};
		});
		$('.js-button-forvard').on('click', function(){
			if($(this).attr('disabled')){
				return false;
			}
			/* find lat post */
			var first_post = $('.js-posts').find('.js-post').first();
			var first = null;
			if(first_post.length) {
				first = parseInt(first_post.data('timestamp')) + 1;
			}
			loadPage(first);
		})
		$('.js-button-back').on('click', function(){
			if($(this).attr('disabled')){
				return false;
			}
			/* find lat post */
			var last_post = $('.js-posts').find('.js-post').last();
			var last = null;
			if(last_post.length) {
				last = parseInt(last_post.data('timestamp')) - 1;
			}
			loadPage(null, last);
		})
		$('.js-button-latest').on('click', function(){
			if($(this).attr('disabled')){
				return false;
			}
			loadPage();
		})
		$(window).on('hashchange', function(d) {
			var params = getHashParams()
			loadPage(params.a, params.b, params.l);
		})
		$('#expand_content_menu, #body_hover').click(function(){
			"use strict";
			var expandAreaWide = jQuery('.left_sidebar_content_area').width();
			if(!$('#expand_content_menu').hasClass('open'))
			{
				$('#expand_content_menu').addClass('open');
				$('#expand_content_menu span').removeClass('icon icon-fontawesome-webfont-1 ');
				$('#expand_content_menu span').addClass('menu_cross');
				$('#expand_content_menu span').html('&times;');
				$('#body_hover').fadeIn(200);
				$('.left_sidebar_content_area').animate({'margin-left':"0px"},100);
				$('.main_content_area').animate({"margin-right":'-'+expandAreaWide+'px'},100);
				if($(window).width()>=768){
					$('#expand_content_menu').animate({left:290},100);
				}
			}
			else{
				$('#expand_content_menu').removeClass('open');
				$('#expand_content_menu span').addClass('icon icon-fontawesome-webfont-1 ');
				$('#expand_content_menu span').removeClass('menu_cross');
				$('#expand_content_menu span').html('');
				$('#body_hover').fadeOut(200);
				$('.left_sidebar_content_area').animate({"margin-left":"-100%"},500);
				$('.main_content_area').animate({"margin-right":'0px'},500);
				if($(window).width()>=768){
					$('#expand_content_menu').animate({left:10},100);
				}
			}
		});
		// ********************** Accordion Code start ******************
		$('.accordion_title').each(function(){
			"use strict";
			var activeIcon = $(this).attr('data-active-icon');
			var DeActiveIcon = $(this).attr('data-deactive-icon');
			$(this).find('.icon').removeClass(activeIcon);
			$(this).find('.icon').addClass(DeActiveIcon);
		})
		$('.panel-heading').click(function(){
			$('.panel-heading').removeClass('active');
			if(!$(this).next('.panel-collapse').hasClass('in')){
				$(this).addClass('active');
			}
			$('.accordion_title').each(function(){
				var activeIcon = $(this).attr('data-active-icon');
				var DeActiveIcon = $(this).attr('data-deactive-icon');
				$(this).find('.icon').removeClass(activeIcon);
				$(this).find('.icon').addClass(DeActiveIcon);
			})
			var activeIcon = $(this).find('.accordion_title').attr('data-active-icon');
			var DeActiveIcon = $(this).find('.accordion_title').attr('data-deactive-icon');
			if($(this).hasClass('active')){
				$(this).find('.icon').removeClass(DeActiveIcon);
				$(this).find('.icon').addClass(activeIcon);
			}
			var activeColor = $(this).find('.accordion_title').css('background-color');
			$(this).next().find('.panel-body').css({"border-color":activeColor});
		});
		// ********************** Accordion Code End ******************
	});
})(jQuery)
