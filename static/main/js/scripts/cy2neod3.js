function Cy2NeoD3(config, graphId, tableId, sourceId, execId, urlSource, renderGraph, cbResult) {
    var neod3 = new Neod3Renderer();
	var neo = new Neo(urlSource);
	$("#"+execId).click(function(evt) {
		try {
			evt.preventDefault();
			var query = "MATCH (n)-[r]->(m) RETURN n,r,m"
			console.log("Executing Query",query);
			var execButton = $(this).find('i');
			execButton.toggleClass('fa-play-circle-o fa-spinner fa-spin')
			neo.executeQuery(query,{},function(err,res) {
				execButton.toggleClass('fa-spinner fa-spin fa-play-circle-o')
				res = res || {}
				var graph=res.graph;
				if (renderGraph) {
					if (graph) {
						var c=$("#"+graphId);
						c.empty();
						neod3.render(graphId, c ,graph);
						//renderResult(tableId, res.table);
					} else {
						if (err) {
							console.log(err);
							if (err.length > 0) {
								sweetAlert("Cypher error", err[0].code + "\n" + err[0].message, "error");
							} else {
								sweetAlert("Ajax " + err.statusText, "Status " + err.status + ": " + err.state(), "error");
							}
						}
					}
				}
				if(cbResult) cbResult(res);
			});
		} catch(e) {
			console.log(e);
			sweetAlert("Catched error", e, "error");
		}
		return false;
	});
    $("#get_path").click(function(evt) {
		    try {
			    evt.preventDefault();
                var first_word = $("#first_word").val()
                var second_word = $("#second_word").val()
                var max_length = $("#max_length").val()
			    var query = "MATCH c=(c1:Notion {name:'" + first_word + "'})-[:depends*1.."+ max_length + "]->(c3:Notion {name:'" + second_word + "'}) RETURN c"
			    console.log("Executing Query",query);
			    var execButton = $(this).find('i');
			    execButton.toggleClass('fa-play-circle-o fa-spinner fa-spin')
			    neo.executeQuery(query,{},function(err,res) {
				    execButton.toggleClass('fa-spinner fa-spin fa-play-circle-o')
				    res = res || {}
				    var graph=res.graph;
				    if (renderGraph) {
					    if (graph) {
						    var c=$("#path_graph");
						    c.empty();
						    neod3.render('path_graph', c ,graph);
						    // renderResult(tableId, res.table);
					    } else {
						    if (err) {
							    console.log(err);
							    if (err.length > 0) {
								    sweetAlert("Cypher error", err[0].code + "\n" + err[0].message, "error");
							    } else {
								    sweetAlert("Ajax " + err.statusText, "Status " + err.status + ": " + err.state(), "error");
							    }
						    }
					    }
				    }
				    if(cbResult) cbResult(res);
			    });
		    } catch(e) {
			    console.log(e);
			    sweetAlert("Catched error", e, "error");
		    }
		    return false;
	    });
}
