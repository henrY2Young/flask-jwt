var vue = new Vue({
    el: '#login-container',
    data() {
        return {
            userForm: {
                username: '',
                password: ''
            },
            loginUrl: '/admin/user/login'
        }
    },
    methods: {
        login() {
            let param = new URLSearchParams();
            param.append('username', this.userForm.username);
            param.append('password', this.userForm.password);
            axios.post(this.loginUrl, param).then(res => {
                console.log(res)
            }).catch(err => {
                console.log(err);
            });
            console.log(this.userForm.password, this.userForm.username);
            alert()
        }
    }
});