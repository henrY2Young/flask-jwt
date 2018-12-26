var gulp = require("gulp");
var less = require("gulp-less");
var auto = require("gulp-autoprefixer");
let  cssmin = require('gulp-minify-css');
let rename = require('gulp-rename');
let lesspatch ='./css/admin/*.less';
let lessdest = './css/admin/';
gulp.task("compileLess", function () {
    gulp.src(lesspatch)
        .pipe(less())
        .pipe(auto({
            grid: true,
            browsers: ['last 2 version']
        }))
        .pipe(cssmin())
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest(lessdest))
});
gulp.task("less", function () {

    gulp.watch(lesspatch, ['compileLess']);

});