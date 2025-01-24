<template>
    <div class = "card_page">
        <div id = "card_name">
            <span>卡名:&nbsp;&nbsp;</span>
            <input v-model = "card_name"/>
        </div>
        <div id = "card_pic">
            <img :src = "card_pic"/>
            <div id = "card_link">
                <img v-for = "(i, v) in [0, 1, 2, 3, 5, 6, 7, 8]" :src = "link_list_pics[i]" :style = "{ 'grid-row-start': [1, 3, 5][Math.floor(i / 3)], 'grid-row-end': [1, 3, 5][Math.floor(i / 3)] + 1, 'grid-column-start': (i % 3) + 1, 'grid-column-end': (i % 3) + 2 }" v-if = "whether_show_links[1] && is_type_link" @mouseover = "change_src(i)" @mouseleave = "reset_src(i)" @click = "change_card_link(i)"/>
            </div>
            <div>
                <button ref = "show_links_btn" @click = "whether_show_or_not_links" :title = "whether_show_links[0]" v-html = "whether_show_links[2]" v-if = "is_type_link"></button>
            </div>
        </div>
        <div id = "card_ot">
            <span>许可:&nbsp;&nbsp;</span>
            <select v-model = "card_ot">
                <option v-for = "(i,v) in ot_list" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_attribute">
            <span>属性:&nbsp;&nbsp;</span>
            <select v-model = "card_attribute">
                <option v-for = "(i,v) in attribute_list" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_level">
            <span>星级:&nbsp;&nbsp;</span>
            <select v-model = "card_level">
                <option v-for = "(i,v) in level_list" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_race">
            <span>种族:&nbsp;&nbsp;</span>
            <select  v-model = "card_race">
                <option v-for = "(i,v) in race_list" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_setcard">
            <span v-for = "(i, v) in Array(4).fill(0)" :key = "v" :style = "{ 'grid-row-start': v + 1, 'grid-row-end': v + 2 }">字段:&nbsp;&nbsp;</span>
            <input v-for = "(i, v) in Array(4).fill(0)" :key = "v" v-model = "card_setcard[v]" @input = "filter_input($event, ['card_setcard', v], /[^a-fA-F0-9]/g)"/>
        </div>
        <div id = "card_id">
            <span>同名卡:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_alias'])" v-model = "card_alias"/>
            <span>卡号:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_id'])" v-model = "card_id"/>
        </div>
        <div id = "card_atk">
            <span>攻击力:&nbsp;&nbsp;</span>
            <input @input = "filter_input($event, ['card_atk'])" v-model = "card_atk"/>
            <span v-if = "!is_type_link">守备力:&nbsp;&nbsp;</span>
            <input v-if = "!is_type_link" @input = "filter_input($event, ['card_def'])" v-model = "card_def"/>
            <span v-if = "is_type_pendulum">灵摆刻度:&nbsp;&nbsp;</span>
            <input v-if = "is_type_pendulum" @input = "filter_input($event, ['card_pendulum'])" v-model = "card_pendulum"/>
        </div>
        <textarea id = "card_desc" v-model = "card_desc"></textarea>
        <div id = "card_box">
            <transition name = "card_type">
                <div v-if = "show_card_box[0][0]" id = "card_type">
                    <button class = "unshow_card_box_btn" @click = "whether_show_card_box(false, 0)" :title = "show_card_box[2][0]">&gt;</button>
                    <h2>卡片类型</h2>
                    <div v-for = "(i, v) in type_list" :key = "v"><span>{{ i[1] }}:&nbsp;</span><input type = "checkbox" v-model = "card_type[v]"/> </div>
                </div>
            </transition>
            <transition name = "card_category">
                <div v-if = "show_card_box[0][1]" id = "card_category">
                    <button class = "unshow_card_box_btn" @click = "whether_show_card_box(false, 1)" :title = "show_card_box[2][1]">&gt;</button>
                    <h2>效果分类</h2>
                    <div v-for = "(i, v) in category_list" :key = "v"><span>{{ i[1] }}:&nbsp;</span><input type = "checkbox" v-model = "card_category[v]"/> </div>
                </div>
            </transition>
            <transition name = "card_hint">
                <div v-if = "show_card_box[0][2]" id = "card_hint" >
                    <button class = "unshow_card_box_btn" @click = "whether_show_card_box(false, 2)" :title = "show_card_box[2][2]">&gt;</button>
                    <h2>脚本提示文字</h2>
                    <div v-for = "(i, v) in Array(16).fill(0)" :key = "v">
                        <span>{{ v }}:&nbsp;</span><input type = "text" v-model = "card_hint[v]"/>
                    </div>
                </div>
            </transition>
            <transition name = "card_box_btn">
                <div v-if = "unshow_card_box" id = "card_box_btn"><button v-for = "(i, v) in Array(3).fill(0)" :key = "v" @click = "whether_show_card_box(true, v)" :title = "show_card_box[1][v]">&lt;</button></div>
            </transition>
        </div>
    </div>
</template>

<script setup name = "card_page">
    import { ref, onMounted, watch, defineEmits, defineProps, computed } from 'vue';
    import axios from 'axios';

    let ot_list = ref([[0x0, '许可 N/A']]);
    let attribute_list = ref([[0x0, '属性 N/A']]);
    let level_list = ref([[0x0, '等级 N/A']]);
    let race_list = ref([[0x0, '种族 N/A']]);
    let type_list = ref([]);
    let category_list = ref([]);
    let link_list = ref([]);

    let link_list_pics = ref([]);
    
    let card_name = ref('');
    let card_ot = ref(ot_list.value[0][1]);
    let card_attribute = ref(attribute_list.value[0][1]);
    let card_level = ref(level_list.value[0][1]);
    let card_race = ref(race_list.value[0][1]);
    let card_id = ref(0);
    let card_alias = ref(0);
    let card_pic = ref('/cover.png');
    let card_atk = ref(0);
    let card_def = ref(0);
    let card_pendulum = ref(0);
    let card_desc = ref('');
    let card_type = ref([]);
    let card_category = ref([]);
    let card_hint = ref([]);
    let card_setcard = ref(Array(4).fill('0'));
    let card_link = ref(0);
    let card_origin_id = ref(0);

    let is_type_link = ref(false);
    let is_type_pendulum = ref(false);
    let whether_show_links = ref(['点击隐藏连接箭头', true, '&#10003']);
    let show_card_box = ref([[false, false, false], ['显示卡片类型', '显示效果分类', '显示卡片脚本提示文字'], ['隐藏卡片类型', '隐藏效果分类', '隐藏卡片脚本提示文字']]);
    let unshow_card_box = ref(true);
    let show_links_btn = ref(null);

    let get_select = defineProps(['cdb', 'page', 'card', 'pic', 'close']);
    let select_card_list = ref([]);
    let new_pic = ref('');
    let close_card = ref(false);

    let emit = defineEmits(['event_close_fixed']);

    let card_data = computed(() => {
        let def_or_link = card_def.value;
        let lv_and_p = level_list.value.find(e => e[1] == card_level.value);
        let setcard_count = parseInt(card_setcard.value.map(e => ('0'.repeat(4 - e.slice(0, 4).length)) + e.slice(0, 4)).join(''), 16);
        let type_count = 0;
        let race_count = race_list.value.find(e => e[1] == card_race.value);
        let attribute_count = attribute_list.value.find(e => e[1] == card_attribute.value);
        let category_count = 0;

        if (lv_and_p)
            lv_and_p = lv_and_p[0];

        if (race_count)
            race_count = race_count[0];
        if (attribute_count)
            attribute_count = attribute_count[0];

        if (card_type.value.length > 0)
            card_type.value.forEach((e, v) => {
                if (e) {
                    type_count += type_list.value[v][0]
                }
            });
        if (card_category.value.length > 0)
            card_category.value.forEach((e, v) => {
                if (e)
                    category_count += category_list.value[v][0]
            });

        if ((type_count & 0x1000000) > 0) {
            lv_and_p |= (card_pendulum.value << 16);
            lv_and_p |= (card_pendulum.value << 24);
        }
        
        if ((type_count & 0x4000000) > 0)
            def_or_link = card_link.value

        return [
            [
                card_id.value,
                card_ot.value,
                card_alias.value,
                card_setcard.value,
                card_type.value,
                card_atk.value,
                card_def.value,
                [card_level.value, card_pendulum.value, card_pendulum.value],
                card_race.value,
                card_attribute.value,
                card_category.value,
                card_id.value,
                card_name.value,
                card_desc.value,
                card_hint.value
            ], [
                card_id.value,
                card_ot.value,
                card_alias.value,
                setcard_count,
                type_count,
                card_atk.value,
                def_or_link,
                lv_and_p,
                race_count,
                attribute_count,
                category_count,
                card_id.value,
                card_name.value,
                card_desc.value
            ].concat(card_hint.value)
        ]
    });

    onMounted(() => {
        for (let i = 1; i < 9; i++) {
            if (i == 5) {
                link_list_pics.value.push('');
            }
            link_list_pics.value.push('./link-arrow/arrow' + i + '.png');
        }
        get_card_info();
    });

    watch(card_data, (new_value) => {
        let type_count = new_value[1][4];
        is_type_pendulum.value = (type_count & 0x1000000) > 0;
        is_type_link.value = (type_count & 0x4000000) > 0;
    }, { deep: true, immediate: true });

    watch(get_select, (new_value) => {
        new_pic.value = new_value.pic;
        close_card.value = new_value.close;
        select_card_list.value[0] = new_value.cdb;
        select_card_list.value[1] = new_value.page;
        select_card_list.value[2] = new_value.card;
    }, { immediate: true });

    watch(new_pic, (n) => {
        if (n.includes(card_id.value) && card_origin_id.value > 0) {
            card_pic.value = n;
        }
    }, { immediate: true });

    watch(close_card, (n) => {
        if (n)
            clear_card();
            emit('event_close_fixed');
    }, { immediate: true });

    watch(select_card_list, (new_value) => {
        if (new_value[0] == '' || new_value[1] == 0)
            return;
        get_card_data();
    }, { immediate: true, deep: true });

    function change_card_link(i) {
        if ((card_link.value & link_list.value[i]) > 0)
            card_link.value -= link_list.value[i]
        else
            card_link.value += link_list.value[i]
        change_src(i)
    }

    function change_src(i) {
        if (link_list_pics.value[i].endsWith('-I.png'))
            return;
        link_list_pics.value[i] = './link-arrow/arrow' + (i < 4? i + 1 : i) + '-I.png'
    }

    
    function reset_src(i) {
        if ((card_link.value & link_list.value[i]) == 0)
            link_list_pics.value[i] = './link-arrow/arrow' + (i < 4? i + 1 : i) + '.png'
    }

    function filter_input(event, t, str_filter = /[^0-9]/) {
        let input_value = event.target.value;
        if (t[0] == 'card_setcard') {
            let new_value = input_value.replace(str_filter, '').slice(0, 4);
            card_setcard.value[t[1]] = new_value;
        } else if (t[0] == 'card_id') {
            let new_value = input_value.replace(str_filter, '').slice(0, 9);
            card_id.value = new_value;
        } else if (t[0] == 'card_alias') {
            let new_value = input_value.replace(str_filter, '').slice(0, 9);
            card_alias.value = new_value;
        } else if (t[0] == 'card_atk') {
            if (input_value.slice(0, 1) == '-' || input_value.slice(0, 1) == '?') {
                card_atk.value = '?';
            } else {
                let new_value = input_value.replace(str_filter, '').slice(0, 19);
                card_atk.value = new_value;
            }
        } else if (t[0] == 'card_def') {
            if (input_value.slice(0, 1) == '-' || input_value.slice(0, 1) == '?') {
                card_def.value = '?';
            } else {
                let new_value = input_value.replace(str_filter, '').slice(0, 19);
                card_def.value = new_value;
            }
        } else if (t[0] == 'card_pendulum') {
            let new_value = input_value.replace(str_filter, '');
            while (new_value != '' && parseInt(new_value) > 15)
                new_value = new_value.slice(0, -1);
            card_pendulum.value = new_value;
        }
    }

    function whether_show_or_not_links() {
        whether_show_links.value[1] = !whether_show_links.value[1];
        whether_show_links.value[0] = whether_show_links.value[1] ? '点击隐藏连接箭头' : '点击显示连接箭头';
        whether_show_links.value[2] = whether_show_links.value[1] ? '&#10003' : '&times';
        if (show_links_btn.value)
            show_links_btn.value.style.backgroundColor = whether_show_links.value[1] ? 'green' : 'red';
    }

    function clear_card() {
        card_name.value = '';
        card_ot.value = ot_list.value[0][1];
        card_attribute.value = attribute_list.value[0][1];
        card_level.value = level_list.value[0][1];
        card_race.value = race_list.value[0][1];
        card_id.value = 0;
        card_alias.value = 0;
        card_pic.value = '/cover.png';
        card_atk.value = 0;
        card_def.value = 0;
        card_pendulum.value = 0;
        card_link.value = 0;
        card_desc.value = '';
        card_type.value = Array(type_list.value.length).fill(false);
        card_category.value = Array(category_list.value.length).fill(false);
        card_hint.value = Array(16).fill('');
        card_setcard.value = Array(4).fill('0');
        card_origin_id.value = 0;
    }

    async function get_card_info() {
        await axios.get('http://127.0.0.1:8000/api/initialize')
            .then(get => {
                ot_list.value = get.data[1];
                attribute_list.value = get.data[2];
                level_list.value = get.data[3];
                link_list.value = get.data[4];
                category_list.value = get.data[5];
                race_list.value = get.data[6];
                type_list.value = get.data[7];
                clear_card()
            })
            .catch(error => {
            console.error('获取数据失败:', error);
        });
    }

    async function get_card_data() {
        try {
            let response = await axios.post('http://127.0.0.1:8000/api/read_card', {
                cdb: select_card_list.value[0],
                page: select_card_list.value[1],
                card: select_card_list.value[2]
            });
            let data = response.data[1];
            cdb_title.value = response.data[0]
            card_id.value = data[0];
            card_ot.value = data[1];
            card_alias.value = data[2];
            card_setcard.value = data[3];
            card_type.value = data[4];
            card_atk.value = data[5];
            card_def.value = data[6];
            card_level.value = data[7][0];
            card_pendulum.value = data[7][1];
            card_race.value = data[8];
            card_attribute.value = data[9];
            card_category.value = data[10];
            card_name.value = data[12];
            card_desc.value = data[13];
            card_hint.value = data[14];
            card_pic.value = data[15];
            card_origin_id.value = data[0];
        } catch (error) {
            console.error('发送请求失败:', error);
        }
    };

    async function whether_show_card_box(chk, v) {
        if (chk) {
            unshow_card_box.value = false;
            await(new Promise(resolve => setTimeout(resolve, 500)));
            show_card_box.value[0][v] = true;
        } else {
            show_card_box.value[0][v] = false;
            await(new Promise(resolve => setTimeout(resolve, 500)));
            unshow_card_box.value = true;
        }
    }
</script>

<style scoped>
    .card_page {
        width: 70vw;
        height: 100vh;

        display: grid;

        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(21, 1fr);

        justify-items: left;

        row-gap: 2vh;
    }

    #card_name {
        grid-column-start: 1;
        grid-column-end: 3;

        justify-self: center;
    }

    #card_ot, #card_attribute, #card_level, #card_race, #card_setcard, #card_id, #card_atk {
        grid-column-start: 2;
        grid-column-end: 3;
    }

    #card_setcard, #card_id , #card_atk{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }

    #card_setcard span, #card_id span, #card_atk span {
        grid-column-start: 1;
        grid-column-end: 2;
    }

    #card_setcard input, #card_id input, #card_atk input {
        grid-column-start: 2;
        grid-column-end: 4;
        width: 80%;
    }

    #card_desc {
        grid-column-start: 1;
        grid-column-end: 3;

        grid-row-start: 9;
        grid-row-end: 16;

        justify-self: center;

        width: 90%;
        height: 100%;

        resize: none;
    }

    #card_pic {
        position: relative;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);

        justify-self: center;
        text-align: center;

        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 2;
        grid-row-end: 8;
    }

    #card_link {
        position: absolute;
        top: 0;
        left: -10%;

        width: 120%;
        height: 100%;

        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(5, 1fr);
        justify-items: center;
    }

    #card_pic img {
        height: 100%;
        width: auto;
        display: block;
    }

    #card_pic button {
        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: green;
    }

    #card_link img {
        height: 100%;
        width: 100%;
    }

    #card_box {
        width: 32vw;
        height: 100vh;
        overflow: hidden;

        grid-column-start: 3;
        grid-column-end: 5;
        grid-row-start: 1;
        grid-row-end: 22;
    }

    #card_type, #card_category {
        display: grid;

        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(16, 1fr);

        justify-items: left;
    }

    #card_category div, #card_type div {
        width: 9vw;

        display: grid;
        grid-template-columns: repeat(3, 1fr);
    }

    #card_category div span, #card_type div span {
        grid-column-start: 1;
        grid-column-end: 3;
        justify-self: center;
    }

    #card_category div input, #card_type div input {
        grid-column-start: 3;
        grid-column-end: 4;
        justify-self: right;

        height: 50%;
        width: 50%;
    }

    .unshow_card_box_btn {
        width: 4vw;
        height: 4vh;

        align-self: center;
        justify-self: left;

        border: none;
        border-radius: 4px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        color: white;
        background-color: green;

        cursor: pointer;

        grid-column-start: 1;
        grid-column-end: 2;
        grid-row-start: 1;
        grid-row-end: 2;
    }

    #card_hint {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(17, 1fr);

        justify-items: left;
    }

    #card_category h2, #card_type h2, #card_hint h2 {
        justify-self: center;
        grid-column-start: 1;
        grid-column-end: 4;
        grid-row-start: 1;
        grid-row-end: 2;
    }

    #card_type, #card_category, #card_hint {
        width: 30vw;
        height: 100vh;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        justify-self: center;
    }

    #card_hint div {
        width: 100%;
        grid-column-start: 1;
        grid-column-end: 4;

        display: grid;
        grid-template-columns: repeat(6, 1fr);
        justify-items: center;
    }

    #card_hint div span {
        align-self: center;
        font-size: 120%;
        grid-column-start: 1;
        grid-column-end: 2;
    }

    #card_hint div input {
        grid-column-start: 2;
        grid-column-end: 7;

        width: 100%;
        height: 80%;
    }

    #card_box_btn {
        right: 0;

        display: grid;
        grid-template-rows: repeat(3, 1fr);
        row-gap: 1vh;
    }

    #card_box_btn button {        
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

    .card_box_btn-enter-active,
    .card_box_btn-leave-active,
    .card_category-enter-active,
    .card_category-leave-active,
    .card_hint-enter-active,
    .card_hint-leave-active,
    .card_type-enter-active,
    .card_type-leave-active {
        transition: transform 0.5s ease;
    }
    .card_category-enter-from,
    .card_category-leave-to,
    .card_hint-enter-from,
    .card_hint-leave-to,
    .card_type-enter-from,
    .card_type-leave-to {
        transform: translateX(100%);
    }
    .card_category-enter-to,
    .card_category-leave-from,
    .card_hint-enter-to,
    .card_hint-leave-from,
    .card_type-enter-to,
    .card_type-leave-from {
        transform: translateX(0%);
    }

    .card_box_btn-enter-to,
    .card_box_btn-leave-from {
        transform: translateX(0%);
    }

    .card_box_btn-enter-from,
    .card_box_btn-leave-to {
        transform: translateX(100%);
    }
</style>
