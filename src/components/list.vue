<template>
    <div class = "list_page">
        <div class = "list_header">
            <h1>{{ list_page.title }}</h1>
            <button id = "unshow_list_page_btn" @click = "whether_show_list_page()" title = "上一级目录">&lt;</button>
            <button id = "close_cdb_btn" @click = "close_cdb()" title = "关闭cdb">&times;</button>
        </div>
        <div class = "list_content">
            <button v-for = "(i,v) in list_page.cdb_list[list_page.page[0]]" :key = "v" @click = "set_select_card(v, $event)" :ref="set_list_btns">{{ i }}</button>
        </div>
        <div class = "list_btn">
            <button ref = "prev_btn" @click = "previous_page">上一页</button>
            <span>第<input @input = "filter_input($event)" v-model = "list_page.page[0]"/>页<br>共{{ list_page.cdb_list.length - 1 }}页</span>
            <button ref = "next_btn" @click = "next_page">下一页</button>
        </div>
    </div>
</template>

<script setup name="list_page" lang = "ts">
    import { ref, reactive, onMounted, watch, defineEmits, defineProps, computed } from 'vue';
    import axios from 'axios';

    let list_page = reactive({
        page: [0],
        selected : -1,
        title: '',
        cdb_list: [],
    });

    let prev_btn = ref(null);
    let next_btn = ref(null);
    let list_btns = [];

    let emit = defineEmits(['event_close_cdb', 'event_select_card', 'event_unshow_list_page']);

    let get_props = defineProps(['cdb']);

    onMounted(() => {
        update_button_styles();
    });

    watch(get_props, (new_value) => {
        if (new_value.cdb[0][0] == '暂未打开cdb')
            return;
        list_page.title = new_value.cdb[0][0];
        list_page.cdb_list = new_value.cdb;
        list_page.page[0] = 1;
        update_button_styles();
    }, { immediate: true });

    watch(list_page.page, () => {
        update_button_styles();
    });

    function filter_input(event) {
        let input_value = event.target.value;
        let new_value = input_value.replace(/[^0-9]/, '');
        while (new_value != '' && parseInt(new_value) >= (list_page.cdb_list.length - 1))
            new_value = new_value.slice(0, -1);
        if (new_value == '')
            new_value = 0;
        list_page.page[0] = new_value;
        list_page.page[0] = new_value;
    }

    function set_select_card(v, event) {
        if (list_page.selected == v) {
            btn_style_change(event.target, '', '');
            emit('event_select_card', list_page.page[0], -1);
            list_page.selected = -1;
        } else {
            if (list_page.selected > -1) {
                btn_style_change(list_btns[list_page.selected], '', '');
            }
            btn_style_change(event.target, 'green', 'white');
            emit('event_select_card', list_page.page[0], v);
            list_page.selected = v;
        }
    }

    function close_cdb() {
        if (confirm('确认关闭cdb吗，此操作可能导致数据丢失'))
            emit('event_close_cdb');
    }

    function whether_show_list_page() {
        emit('event_unshow_list_page');
    }

    function next_page() {
        if (list_page.page[0] < list_page.cdb_list.length - 1) {
            list_page.page[0] ++ ;
            if (list_page.selected > -1) {
                btn_style_change(list_btns[list_page.selected], '', '');
                list_page.selected = -1
            }
        }
    }

    function previous_page() {
        if (list_page.page[0] > 1) {
            list_page.page[0] -- ;
            if (list_page.selected > -1) {
                btn_style_change(list_btns[list_page.selected], '', '');
                list_page.selected = -1
            }
        }
    }

    function update_button_styles() {
        btn_style_change(prev_btn.value, 'green', 'white');
        btn_style_change(next_btn.value, 'green', 'white');
        if (list_page.page[0] <= 1)
            btn_style_change(prev_btn.value, 'gray', 'black');
        if (list_page.page[0] >= list_page.cdb_list.length - 1)
            btn_style_change(next_btn.value, 'gray', 'black');
    }

    function btn_style_change(btn, btn_color, text_color) {
        if (!btn) return;
        btn.style.backgroundColor = btn_color;
        btn.style.color = text_color;
    }

    function set_list_btns(el) {
        if (!el) return;
        list_btns.push(el);
    }

</script>

<style scoped>
    .list_page {
        width: 30vw;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        display: grid;
    }

    .list_header {
        height: 10vh;
        width: 30vw;
        
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(2, 1fr);
    }

    .list_header h1 {
        grid-column-start: 1;
        grid-column-end: 4;
        grid-row-start: 1;
        grid-row-end: 3;
    }

    #unshow_list_page_btn {
        width: 4vw;
        height: 4vh;

        align-self: center;
        justify-self: right;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: green;

        cursor: pointer;
    }

    #close_cdb_btn {
        width: 4vw;
        height: 4vh;

        align-self: center;
        justify-self: right;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: red;

        cursor: pointer;
    }

    .list_content {
        height: 80vh;
    }

    .list_content button {
        display: grid;

        width: 30vw;
        height: 8vh;

        align-items:  center;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .list_content button:hover {
        width: 31vw;
        color: white;
        background-color: green;
    }

    .list_btn {
        display: flex;
        align-items:  center;
    }

    .list_btn button {
        width: 10vw;
        height: 8vh;
        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);

        cursor: pointer;
    }

    .list_btn span {
        width: 10vw;
        height: 8vh;
        text-align: center;
    }

    .list_btn input {
        width: 3vw;
    }
</style>