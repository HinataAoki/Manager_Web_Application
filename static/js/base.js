var STORAGE_KEY = 'todos-vuejs-demo'
var todoStorage = {
fetch: function() {
    var todos = JSON.parse(
    localStorage.getItem(STORAGE_KEY) || '[]'
    )
    todos.forEach(function(todo, index) {
    todo.id = index
    })
    todoStorage.uid = todos.length
    return todos
},
save: function(todos) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(todos))
}
}

const app = new Vue({
    el:'#app',
    data:{
        //使用するデータ
        secondary:true,
        high:false,
        first:true,
        second:false,
        third:false,
        rank:'中学'
    },
    methods:{
        //使用するメソッド
        click_main:function(){
            if(this.secondary==true)
            {
                this.secondary=false
                this.high=true
                this.rank='高校'
            }
            else if(this.high==true)
            {
                this.secondary=true
                this.high=false
                this.rank='中学'
            }
        },
        click_sub:function(){
            if(this.first==true)
            {
                this.first=false,
                this.second=true,
                this.third=false
            }
            else if(this.second==true)
            {
                this.first=false,
                this.second=false,
                this.third=true
            }
            else if(this.third==true)
            {
                this.first=true,
                this.second=false,
                this.third=false
            }
        }
    }
})

$(function() {
    var $children = $('.children');
    var original = $children.html();

    $('.parent').change(function() {
        var val1 = $(this).val();

        $children.html(original).find('option').each(function() {
        var val2 = $(this).data('val');
        if (val1 != val2) {
            $(this).not('optgroup,.msg').remove();
        }
        });

        if ($(this).val() === '') {
        $children.attr('disabled', 'disabled');
        } else {
        $children.removeAttr('disabled');
        }

    });
});