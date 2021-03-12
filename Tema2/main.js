const http = require("http");
const host = 'localhost';
const port = 8000;
const mongoose = require("mongoose");
const dbURI  = "mongodb+srv://emanuel:admin@cluster0.o3hap.mongodb.net/Node?retryWrites=true&w=majority"
const Cat = require("./models/cats")


async function patchcat(url, body, response){
    if(url === '/cats'){
        response.statusCode = 405;
        response.end("Not allowed!");
    }else{
        if(url.substr(0,6) === '/cats/') {
            let catName = url.substr(6);
            const catObj = JSON.parse(body.toString());
            if( catObj.name != null && catObj.owner != null)
            {
                Cat.findOneAndUpdate({name: catName}, {name: catObj.name, owner: catObj.owner}, function (err, docs) {
                    if (err) {
                        //console.log(err)
                        response.statusCode = 404;
                        response.end("Not found!");
                    } else {
                        if (docs === null) {
                            response.statusCode = 404;
                            response.end("Not found!");
                        } else {
                            response.statusCode = 200;
                            response.end("Patch successful.");
                        }
                    }
                });
            }else{
                if (catObj.name != null){
                    Cat.findOneAndUpdate({name: catName}, {name: catObj.name}, function (err, docs) {
                        if (err) {
                            //console.log(err)
                            response.statusCode = 404;
                            response.end("Not found!");
                        } else {
                            if (docs === null) {
                                response.statusCode = 404;
                                response.end("Not found!");
                            } else {
                                response.statusCode = 200;
                                response.end("Patch successful.");
                            }
                        }
                    });
                } else {
                    if(catObj.owner != null){
                        Cat.findOneAndUpdate({name: catName}, {owner: catObj.owner}, function (err, docs) {
                            if (err) {
                                //console.log(err)
                                response.statusCode = 404;
                                response.end("Not found!");
                            } else {
                                if (docs === null) {
                                    response.statusCode = 404;
                                    response.end("Not found!");
                                } else {
                                    response.statusCode = 200;
                                    response.end("Patch successful.");
                                }
                            }
                        });
                    } else{
                        response.statusCode = 400;
                        response.end();
                    }
                }
            }
            }
    }
}

async function getcat(url, response){
    if (url === '/cats'){
        try{
        Cat.find({},function (err, cats){
            if (err){
                console.log(err);
            }else{
                response.statusCode = 200;
                response.setHeader('Content-Type', 'application/json')
                response.write("{cats: " + cats.toString() + '}');
                response.end();
            }
        });}
        catch (err){
            console.log(err);
            response.statusCode =  500;
            response.end();
        }
    }else{
        if(url.substr(0,6) === '/cats/'){
            let catName = url.substr(6);
            console.log(catName);
            try{
                Cat.find({name:catName},function (err, cats){
                    if (err){
                        console.log(err);
                    }else{
                        if (cats.toString().length >10){
                        response.statusCode = 200;
                        response.setHeader('Content-Type', 'application/json')
                        response.write("{cats: " + cats.toString() + '}');
                        response.end();}
                        else{
                            response.statusCode = 404;
                            response.end();
                        }
                    }
                });}
            catch (err){
                console.log(err);
                response.statusCode =  404;
                response.end();
            }
        }else{
            console.log(url);
            response.statusCode = 400;
            response.end();
        }
    }
    return 0;
}

async function postcat(url, body, response){
    if (url == '/cats'){
        var cat_collection = JSON.parse(body.toString());
        //console.log(cat_collection.cats[0].toString());
        var manycats = new Array();
        for(let index = 0; index < cat_collection.cats.length; index++){
            const cat = new Cat({name:cat_collection.cats[index].name, owner:cat_collection.cats[index].owner});
            manycats.push(cat);
        }
         Cat.insertMany(manycats).then(function (docs) {
             response.statusCode = 201;
             response.setHeader('Content-Type', 'application/json')
             response.setHeader('Location','http://localhost:8000/cats')
             response.write("{ " + docs.toString() + '}');
             response.end();
        }).catch(function (err){
            response.statusCode = 409;
            response.end();
         });
    }else{
        if(url.substr(0,6) === '/cats/'){
            const cat_text = JSON.parse(body.toString());
            const cat = new Cat({
                name: cat_text.name,
                owner: cat_text.owner
            });
            cat.save().then(r => {
                    response.statusCode = 201;
                    response.setHeader('Location','http://localhost:8000/cats/' + cat_text.name);
                    response.end();
                }).catch(err=>{
                    response.statusCode = 409;
                    response.end();
            });
        }
    }
    return 0;
}

async function deletecat(url, response){
    if(url === '/cats'){
        response.statusCode = 405;
        response.end("Not allowed!");
    }else{
        if(url.substr(0,6) === '/cats/') {
            let catName = url.substr(6);
            Cat.findOneAndDelete({name:catName}, function (err, docs){
                if(err){
                    response.statusCode = 404;
                    response.end("Not found!");
                }else{
                    if(docs === null){
                        response.statusCode = 404;
                        response.end("Not found!");
                    }else{
                        response.statusCode = 200;
                        response.end("Delete successful.");
                    }
                }
            });
        }
    }
}

async function putcat(url, body, response){
    if(url === '/cats'){
        response.statusCode = 405;
        response.end("Not allowed!");
    }else{
        if(url.substr(0,6) === '/cats/') {
            let catName = url.substr(6);
            const catObj = JSON.parse(body.toString());
            console.log(catObj.name,catObj.owner);
            Cat.findOneAndUpdate({name:catName}, {name: catObj.name, owner : catObj.owner}, function (err, docs){
                if(err){
                    //console.log(err)
                    response.statusCode = 404;
                    response.end("Not found!");
                }else{
                    if(docs === null){
                        response.statusCode = 404;
                        response.end("Not found!");
                    }else{
                        response.statusCode = 200;
                        response.end("Put successful.");
                    }
                }
            });
        }
    }
}

async function notfound(request, response){
    response.statusCode = 405;
    response.end();
}

const requestListener = function (request, response) {
    const { headers, method, url } = request;
    let body = [];
    request.on('error', (err) => {
        console.error(err);
    }).on('data', (chunk) => {
        body.push(chunk);
    }).on('end', () => {
        body = Buffer.concat(body).toString();
        switch (method){
            case 'GET':
                getcat(url, response);
                break;
            case 'PUT':
                putcat(url, body, response);
                break;
            case 'POST':
                postcat(url, body, response);
                break;
            case 'DELETE':
                deletecat(url, response);
                break;
            case 'PATCH':
                patchcat(url, body, response);
                break;
            default:
                notfound(url, response);
        }
    });


    // const cat = new Cat({
    //     name: "somestr",
    //     owner: "anotherstr"
    // });
    // cat.save().then(r => {
    //     response.writeHead(200);
    //     response.end("My first server!");
    // }).catch(err=>console.log(err));

};
const server = http.createServer(requestListener);
mongoose.connect(dbURI, {useNewUrlParser: true, useUnifiedTopology: true}).then(results =>
    server.listen(port, host, () => {
    console.log(`Server is running on http://${host}:${port}`);
}))
    .catch(err=>console.log(err));

