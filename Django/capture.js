var system = require('system');

function capture(array){
	var page = require('webpage').create();
	page.settings = {
			javascriptEnabled:true,
			loadImages:true,
			resourceTimeout:8000,
	};
	page.settings.viewportSize = {width:1000};
	page.open(array[0], function(success){
	    if(success==='success'){        
	        page.render(array[1]);
	        // console.log('success');
	        phantom.exit();
	    }else{
	        // console.log('error');
	        phantom.exit();
	    }
	});
}

if ( system.args.length < 2 ) {
    console.log("Enter a valid link and a file name !!!");
    phantom.exit(1);
} else {
    capture(system.args.slice(1), function() {
        phantom.exit();
    });
}