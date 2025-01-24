<template>
    <div class = "list_page">
        <div class = "list_header">
            <h1>{{ title }}</h1>
            <button id = "unshow_list_page_btn" @click = "whether_show_list_page()" title = "上一级目录">&lt;</button>
            <button id = "close_cdb_btn" @click = "close_cdb()" title = "关闭cdb">&times;</button>
        </div>
        <div class = "list_content">
            <button v-for = "(i,v) in cdb_list[page]" :key = "v" @click = "set_select_card(v, $event)" :ref="set_list_btns">{{ i }}</button>
        </div>
        <div class = "list_btn">
            <button ref = "prev_btn" @click = "previous_page">上一页</button>
            <span>第<input @input = "filter_input($event)" v-model = "page"/>页<br>共{{ cdb_list.length - 1 }}页</span>
            <button ref = "next_btn" @click = "next_page">下一页</button>
        </div>
    </div>
</template>

<script setup name="list_page">
    import { ref, onMounted, watch, defineEmits, defineProps, computed } from 'vue';
    import axios from 'axios';

    let page = ref(0)
    let title = ref('');
    let cdb_list = ref([]);
    let prev_btn = ref(null);
    let next_btn = ref(null);

    let emit = defineEmits(['event_close_cdb', 'event_select_card', 'event_unshow_list_page']);

    let selected = -1;
    let list_btns = [];

    let get_props = defineProps(['cdb']);

    onMounted(() => {
        update_button_styles();
    });

    watch(get_props, (new_value) => {
        if (new_value.cdb[0][0] == '暂未打开cdb')
            return;
        title.value = new_value.cdb[0][0];
        cdb_list.value = new_value.cdb;
        page.value = 1;
        update_button_styles();
    }, { immediate: true });

    watch(page, () => {
        update_button_styles();
    });

    function filter_input(event) {
        let input_value = event.target.value;
        let new_value = input_value.replace(/[^0-9]/, '');
        while (new_value != '' && parseInt(new_value) >= (cdb_list.value.length - 1))
            new_value = new_value.slice(0, -1);
        if (new_value == '')
            new_value = 0;
        page.value = new_value;
        page.value = new_value;
    }

    function set_select_card(v, event) {
        if (selected == v) {
            btn_style_change(event.target, '', '');
            emit('event_select_card', page.value, -1);
            selected = -1;
        } else {
            if (selected > -1) {
                btn_style_change(list_btns[selected], '', '');
            }
            btn_style_change(event.target, 'green', 'white');
            emit('event_select_card', page.value, v);
            selected = v;
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
        if (page.value < cdb_list.value.length - 1) {
            page.value ++ ;
            if (selected > -1) {
                btn_style_change(list_btns[selected], '', '');
                selected = -1
            }
        }
    }

    function previous_page() {
        if (page.value > 1) {
            page.value -- ;
            if (selected > -1) {
                btn_style_change(list_btns[selected], '', '');
                selected = -1
            }
        }
    }

    function update_button_styles() {
        btn_style_change(prev_btn.value, 'green', 'white');
        btn_style_change(next_btn.value, 'green', 'white');
        if (page.value <= 1)
            btn_style_change(prev_btn.value, 'gray', 'black');
        if (page.value >= cdb_list.value.length - 1)
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