const express = require('express')
const app = express()
const router = express.Router()
const bodyParser = require('body-parser')
const mysql = require('mysql');

// まずはルーティングのみ追加
router.post(
  '/webhook',
  // 署名検証のためテキストでパース
  bodyParser.text({ type: 'application/json' }),
  require('./routes/webhook')
)

// databaseの接続
router.get('/database', (req, res, next) => {
  // const mysql = require('promise-mysql');
  const connection = mysql.createConnection({
    // host : `${process.env.MYSQL_HOST_ADDRESS}`,
    host : '192.168.100.66',
    user : 'test_mac',
    port : "3306",
    password: 'InfoNetworking',
    database: 'scraping',
  });
  var ret=[];
  // connection.connect((err) => {
  // if (err) {
  //   console.log('error connecting: ' + err.stack);
  //   return;
  // }
  // console.log('success');
  // });
  connection.query('SELECT * from cloud_data;', function(error, row, fields){
    if (error) {
      console.log(req)
      console.log(error);
    }
    var dat = [];
    for (var i = 0;i < row.length; i++) {
      dat.push({id: row[i].id, name: row[i].img_name});
    }
    ret = JSON.stringify(dat);
    res.header('Content-Type', 'application/json; charset=utf-8')
    res.send(ret)
  });
  connection.end();
})

module.exports = router