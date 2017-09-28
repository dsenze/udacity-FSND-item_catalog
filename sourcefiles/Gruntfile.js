module.exports = function(grunt) {
    require('load-grunt-tasks', 'grunt-jsbeautifier', 'grunt-contrib-cssmin', 'grunt-contrib-copy', 'imagemin-mozjpeg', 'grunt-flake8')(grunt);
    grunt.initConfig({
        jsbeautifier: {
            // this fix html layout, but destroys flask templates. TODO.
            files: ["templates/*.html"],
            options: {
                html: {
                    braceStyle: "collapse",
                    indentChar: " ",
                    indentScripts: "keep",
                    indentSize: 4,
                    maxPreserveNewlines: 10,
                    preserveNewlines: true,
                    unformatted: ["a", "sub", "sup", "b", "i", "u"],
                    wrapLineLength: 0
                },
            }
        },
        copy: {
            pythonfiles: {
                expand: true,
                src: '*.py',
                dest: 'tempdist/',
            },
            moveToProd: {
                expand: true,
                cwd: 'tempdist/',
                src: ['**'],
                dest: '../',
            },
        },
        cssmin: {
            target: {
                files: [{
                    expand: true,
                    cwd: '',
                    src: ['static/css/*.css', '!*min.css'],
                    dest: 'tempdist/',
                    ext: '.css'
                }]
            },
        },
        imagemin: {
            dynamic: {
                files: [{
                    expand: true,
                    cwd: '',
                    src: ['static/images/**/*.{png,jpg,gif}'],
                    dest: 'tempdist/'
                }]
            }
        },
        flake8: {
            options: {
                maxLineLength: 120,
                maxComplexity: 10,
                format: 'pylint',
                hangClosing: true,
            },
            src: ['**/*.py']
        },

    });

    grunt.registerTask('default', [
        'flake8',
        'cssmin',
        'imagemin',

    ]);
};