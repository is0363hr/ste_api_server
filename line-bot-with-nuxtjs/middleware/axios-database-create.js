import axios from 'axios'

const instance = axios.create({
  baseURL: `${process.env.LOCAL_URL}/api`,
})

// axios.get('/database', (req, res, next) => {
//   const mysql = require('mysql');
//   const connection = mysql.createConnection({
//     // host : `${process.env.LOCAL_URL}/api`,
//     host : '192.168.100.66',
//     user : 'test',
//     port : "3306",
//     password: 'InfoNetworking',
//     database: 'scraping',
//   });
//   var ret=[];
//   connection.connect();
//   connection.query('SELECT * from cloud_data;', function(error, row, fields){
//     if (error) {
//       console.log(error);
//     }
//     var dat = [];
//     for (var i = 0;i < row.length; i++) {
//       dat.push({id: row[i].id, name: row[i].img_name});
//     }
//     ret = JSON.stringify(dat);
//     res.header('Content-Type', 'application/json; charset=utf-8')
//     res.send(ret)
//   });
//   connection.end();
// })

export default instance