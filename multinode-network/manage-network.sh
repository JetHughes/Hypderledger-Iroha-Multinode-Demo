function up(){

    echo up
    docker-compose -f network/docker-compose.yaml up -d
}

function pause(){
    docker-compose -f network/docker-compose.yaml pause
}

function unpause(){
    docker-compose -f network/docker-compose.yaml unpause
}
function down(){

    docker-compose -f network/docker-compose.yaml down --volumes --remove-orphans
}

function restart(){
    down
    up
}

"$@"