<template>
    <div class = "card_page">
        <div id = "card_name">
            <span>卡名:&nbsp;&nbsp;</span>
            <input v-model = "card.name"/>
            <span>&nbsp;&nbsp;</span>
            <el-button @click = "card.search()">
                <el-icon><search/></el-icon>
                <span>搜索</span>
            </el-button>
        </div>
        <div id = "card_pic">
            <pic :style = "{ 'display': card.pic != '' ? 'none' : '' }"/>
            <img :src = "card.pic" v-if = "card.pic != ''"/>
            <div id = "card_link">
                <img v-for = "(i, v) in [0, 1, 2, 3, 5, 6, 7, 8]" :src = "lists.link_pics[i]" :style = "{ 'grid-row-start': [1, 3, 5][Math.floor(i / 3)], 'grid-row-end': [1, 3, 5][Math.floor(i / 3)] + 1, 'grid-column-start': (i % 3) + 1, 'grid-column-end': (i % 3) + 2 , 'display': vif.show.link.chk && vif.is_type.link ? 'block' : 'none' }" @mouseover = "card.get_link.src.get(i)" @mouseleave = "card.get_link.src.reset(i)" @click = "card.get_link.link(i)"/>
            </div>
            <div>
                <el-switch v-if = "vif.is_type.link" v-model = "vif.show.link.chk"></el-switch>
            </div>
        </div>
        <div id = "card_ot">
            <span>&nbsp;&nbsp;许可:</span>
            <select v-model = "card.ot">
                <option v-for = "(i,v) in lists.ot" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_attribute">
            <span>&nbsp;&nbsp;属性:</span>
            <select v-model = "card.attribute">
                <option v-for = "(i,v) in lists.attribute" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_level">
            <span>&nbsp;&nbsp;星级:</span>
            <select v-model = "card.level">
                <option v-for = "(i,v) in lists.level" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_race">
            <span>&nbsp;&nbsp;种族:</span>
            <select  v-model = "card.race">
                <option v-for = "(i,v) in lists.race" :key = "v" >{{ i[1] }}</option>
            </select>
        </div>
        <div id = "card_setcard">
            <div v-for = "(i, v) in Array(4).fill(0)" :key = "v">
                <span style = "grid-column-start: 1; grid-column-end: 2;">&nbsp;&nbsp;字段:</span>
                <input v-model = "card.setcard[v]" @input = "filter_input($event, ['card_setcard', v], /[^a-fA-F0-9]/g)" @change = "card_change.setcard(v)" style = "grid-column-start: 2; grid-column-end: 3; width: 80%;"/>
                <input v-model = "card_n.setcard_name[v]" @change = "card_change.setcard_name(v)" style = "grid-column-start: 3; grid-column-end: 4; width: 80%;" :readonly = "lists.setcard.find(i => i[0] == card.setcard[v]) != undefined"/>
            </div>
        </div>
        <div id = "card_id">
            <span>&nbsp;&nbsp;同名卡:</span>
            <input @input = "filter_input($event, ['card_alias'])" v-model = "card.alias"/>
            <span>&nbsp;&nbsp;卡号:</span>
            <input @input = "filter_input($event, ['card_id'])" v-model = "card.id"/>
            <strong v-if = "vif.warn.same_id">*卡号已存在</strong>
        </div>
        <div id = "card_atk">
            <span>&nbsp;&nbsp;攻击力:</span>
            <input @input = "filter_input($event, ['card_atk'])" v-model = "card.atk"/>
            <span v-if = "!vif.is_type.link">&nbsp;&nbsp;守备力:</span>
            <input v-if = "!vif.is_type.link" @input = "filter_input($event, ['card_def'])" v-model = "card.def"/>
            <span v-if = "vif.is_type.pendulum">&nbsp;&nbsp;灵摆刻度:</span>
            <input v-if = "vif.is_type.pendulum" @input = "filter_input($event, ['card_pendulum'])" v-model = "card.pendulum"/>
        </div>
        <textarea id = "card_desc" v-model = "card.desc"></textarea>
        <div id = "card_box_btn">
            <el-button @click = "card.add()">
                <el-icon><DocumentAdd/></el-icon>
                <span>新建</span>
            </el-button>
            <el-button @click = "card.del()">
                <el-icon><Delete/></el-icon>
                <span>删除</span>
            </el-button>
            <el-button @click = "copy.from()">
                <el-icon><CopyDocument/></el-icon>
                <span>复制</span>
            </el-button>
            <el-button @click = "copy.to()">
                <el-icon><DocumentCopy/></el-icon>
                <span>黏贴</span>
            </el-button>
            <download/>
            <!-- <button style = "background-color: cornflowerblue;">设置</button> -->
        </div>
        <div id = "card_right">
            <transition name = "card_right">
                <div v-if = "vif.show.type.chk" id = "card_type">
                    <el-button @click = "whether_show_rpage('pic')" class = "change_rpage_btn">
                        <el-icon><Picture/></el-icon>
                        <span>{{ vif.show.pic.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('type')" class = "change_rpage_btn" style = "background-color: #ecf5ff; order: 0.01px solid #409eff; color: #409eff;">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.type.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('category')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.category.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('hint')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.hint.title }}</span>
                    </el-button>
                    <div v-for = "(i, v) in lists.type" :key = "v" @change = "card_change.type(v)"><span>{{ i[1] }}:&nbsp;</span><input type = "checkbox" v-model = "card.type[v]"/> </div>
                </div>
            </transition>
            <transition name = "card_right">
                <div v-if = "vif.show.category.chk" id = "card_category">
                    <el-button @click = "whether_show_rpage('pic')" class = "change_rpage_btn">
                        <el-icon><Picture/></el-icon>
                        <span>{{ vif.show.pic.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('type')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.type.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('category')" class = "change_rpage_btn" style = "background-color: #ecf5ff; order: 0.01px solid #409eff; color: #409eff;">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.category.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('hint')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.hint.title }}</span>
                    </el-button>
                    <div v-for = "(i, v) in lists.category" :key = "v" @change = "card_change.category(v)"><span>{{ i[1] }}:&nbsp;</span><input type = "checkbox" v-model = "card.category[v]"/> </div>
                </div>
            </transition>
            <transition name = "card_right">
                <div v-if = "vif.show.hint.chk" id = "card_hint" >
                    <el-button @click = "whether_show_rpage('pic')" class = "change_rpage_btn">
                        <el-icon><Picture/></el-icon>
                        <span>{{ vif.show.pic.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('type')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.type.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('category')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.category.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('hint')" class = "change_rpage_btn" style = "background-color: #ecf5ff; order: 0.01px solid #409eff; color: #409eff;">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.hint.title }}</span>
                    </el-button>
                    <div v-for = "(i, v) in Array(16).fill(0)" :key = "v">
                        <span>{{ v }}:&nbsp;</span><input type = "text" v-model = "card.hint[v]"/>
                    </div>
                </div>
            </transition>
            <transition name = "card_right">
                <div v-if = "vif.show.pic.chk" id = "card_pic_setting" >
                    <el-button @click = "whether_show_rpage('pic')" class = "change_rpage_btn" style = "background-color: #ecf5ff; order: 0.01px solid #409eff; color: #409eff;">
                        <el-icon><Picture/></el-icon>
                        <span>{{ vif.show.pic.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('type')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.type.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('category')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.category.title }}</span>
                    </el-button>
                    <el-button @click = "whether_show_rpage('hint')" class = "change_rpage_btn">
                        <el-icon><Fold/></el-icon>
                        <span>{{ vif.show.hint.title }}</span>
                    </el-button>
                    <el-switch
                        v-model = "vif.show.pic_cut.cut_or_set"
                        active-text = "设置"
                        inactive-text = "卡图裁切"
                        style = "grid-column-start: 1; grid-column-end: 5; justify-self: center;"
                        @change = "upload_file.resert()"
                    />
                    <transition name = "card_right">
                        <div class = "card_pic_setting_content" v-if = "vif.show.pic_cut.cut_or_set">
                            <span>&nbsp;&nbsp;圆角:</span>
                            <el-switch v-model="pic_setting.radius"/>
                            <span>&nbsp;&nbsp;描述居中:</span>
                            <el-switch v-model="pic_setting.descriptionAlign"/>
                            <span>&nbsp;&nbsp;首行压缩:</span>
                            <el-switch v-model="pic_setting.firstLineCompress"/>
                            <span>&nbsp;&nbsp;文字缩放:</span>
                            <el-input-number v-model = "pic_setting.descriptionZoom" :min = "0" :max = "1" :step = "0.01"></el-input-number>
                            <span>&nbsp;&nbsp;字重:</span>
                            <el-input-number v-model = "pic_setting.descriptionWeight" :min = "0" :max = "1" :step = "0.1"></el-input-number>
                            <span>&nbsp;&nbsp;版权:</span>
                            <el-select v-model = "pic_setting.copyright" placeholder = "">
                                <el-option label = "无" value = "" />
                                <el-option label = "简体中文" value = "sc" />
                                <el-option label = "日文" value = "jp" />
                                <el-option label = "英文" value = "en" />
                            </el-select>
                            <span>&nbsp;&nbsp;角标:</span>
                            <el-select v-model = "pic_setting.laser" placeholder = "">
                                <el-option label = "无" value = "" />
                                <el-option label = "样式一" value = "laser1" />
                                <el-option label = "样式二" value = "laser2" />
                                <el-option label = "样式三" value = "laser3" />
                                <el-option label = "样式四" value = "laser4" />
                            </el-select>
                            <span>&nbsp;&nbsp;罕贵:</span>
                            <el-select v-model = "pic_setting.rare" placeholder = "">
                                <el-option label = "无" value = "" />
                                <el-option label = "DT" value = "dt" />
                                <el-option label = "UR" value = "ur" />
                                <el-option label = "GR" value = "gr" />
                                <el-option label = "HR" value = "hr" />
                                <el-option label = "SER" value = "ser" />
                                <el-option label = "GSER" value = "gser" />
                                <el-option label = "PSER" value = "pser" />
                            </el-select>
                            <span>&nbsp;&nbsp;卡包:</span>
                            <el-input v-model = "pic_setting.package"></el-input>
                        </div>
                    </transition>
                    <transition name = "card_right">
                        <div class = "card_pic_setting_content" v-if = "!vif.show.pic_cut.cut_or_set">
                            <div style = "width: 30vw; grid-column-start: 1; grid-column-end: 4;">
                                <div id = "upload_area" @dragenter.prevent="upload_file.uploading = true" @dragover.prevent="upload_file.uploading = true" @dragleave.prevent="upload_file.uploading = false" @drop.prevent="upload_file.drag" @click="() => { upload_file_input.click(); }">
                                    <h4>上传中心图</h4>
                                    <input type = "file" accept = "image/*" ref = "upload_file_input" @change = "upload_file.click" style = "display: none;"/>
                                </div>
                            </div>
                            <pic_cut style = "grid-column-start: 1; grid-column-end: 4; grid-row-start: 3; grid-row-end: 18;"/>
                        </div>
                    </transition>
                </div>
            </transition>
        </div>
    </div>
</template>

<script setup name = "card_page" lang = "ts">
    import { ref, reactive, onMounted, onBeforeMount, watch, defineEmits, defineProps, computed, TrackOpTypes, toRaw } from 'vue';
    import axios from 'axios';
    import emitter from '@/utils/emitter';

    import download from './download.vue'
    import pic from './pic.vue'
    import pic_cut from './pic_cut.vue'

    let lists = reactive({
        ot: [[0x0, '许可 N/A']],
        attribute: [[0x0, '属性 N/A']],
        level: [[0x0, '等级 N/A']],
        race: [[0x0, '种族 N/A']],
        type: [] as [number , string][],
        category: [] as [number , string][],
        link: [] as number[],
        link_pics: [] as string[],
        setcard : [] as string[],
        custom_setcard : [] as [string, string][],
        get : async function() {
            try {
                let response = await axios.get(`${window.location.href}api/initialize`)
                    lists.ot = response.data[1];
                    lists.attribute = response.data[2];
                    lists.level = response.data[3];
                    lists.link = response.data[4];
                    lists.category = response.data[5];
                    lists.race = response.data[6];
                    lists.type = response.data[7];
                    card.clear();
            } catch(error) {};
        }
    });
    
    let card = reactive({
        name : '',
        desc : '',
        pic : '',
        center_pic : '',
        id : 0,
        alias : 0,
        pendulum : 0,
        link : 0,
        origin_id : 0,
        origin_name : '',
        ot : '',
        attribute : '',
        level : '',
        race : '',
        atk : 0 as number | string,
        def : 0 as number | string,
        type : [false],
        category : [false],
        hint : [''],
        setcard : Array(4).fill('0'),
        setcard_name : Array(4).fill(''),
        get_link : {
            link : function(i) {
                if ((card.link & lists.link[i]) > 0)
                    card.link -= lists.link[i]
                else
                    card.link += lists.link[i]
                card.get_link.src.get(i);
            } as (i: number) => void,
            src : {
                get : function(i) {
                    if (lists.link_pics[i].endsWith('-on.png'))
                        return;
                    lists.link_pics[i] = './link-arrow/arrow-' + (i < 4? i + 1 : i) + '-on.png'
                } as (i: number) => void,
                reset : function (i) {
                    if ((card.link & lists.link[i]) == 0)
                        lists.link_pics[i] = './link-arrow/arrow-' + (i < 4? i + 1 : i) + '-off.png'
                } as (i: number) => void
            }
        },
        search : function() {
            select.id = -1;
            emit.list_page.search.to([
                card_n.id,
                card_n.ot,
                card_n.alias,
                card.setcard,
                card_n.type,
                card_n.atk,
                card_n.def,
                card_n.level,
                card_n.race,
                card_n.attribute,
                card_n.category,
                card_n.id,
                card.name,
                card.desc
            ].concat(card.hint));
        },
        clear : function() {
            card.name = '';
            card.ot = lists.ot[0][1] as string;
            card.attribute = lists.attribute[0][1] as string;
            card.level = lists.level[0][1] as string;
            card.race = lists.race[0][1] as string;
            card.id = 0;
            card.alias = 0;
            card.pic = '';
            card.center_pic = '';
            card.atk = 0;
            card.def = 0;
            card.pendulum = 0;
            card.link = 0;
            card.desc = '';
            card.type = Array(lists.type.length).fill(false);
            card.category = Array(lists.category.length).fill(false);
            card.hint = Array(16).fill('');
            card.setcard = Array(4).fill('0');
            card.origin_id = 0;
            card.origin_name = '';
            select.id = -1;
            card_n.type = 0;
            card_n.category = 0;
        } as () => void,
        del : async function() {
            if (open.cdb == '') return;
            if (select.id <= 0) {
                emit.main_page.cdb_closed.to();
                return;
            }
            await card.data.del();
            card.clear();
            emit.list_page.cdb_changed.to();
        } as () => void,
        add: async function() {
            if (open.cdb == '') {
                emit.main_page.cdb_add.to();
                return;
            } else {
                let response = await card.data.add();
                await card.data.save('add');
                emit.list_page.cdb_changed.to(response);
            }
        } as () => void,
        data : {
            get : async function () {
                try {
                    let response = await axios.post(`${window.location.href}api/read_card`, {
                        cdb: open.cdb,
                        id: select.id,
                    });
                    let data = response.data;
                    card.origin_id = data[0];
                    card.id = data[0];
                    card.ot = data[1];
                    card.alias = data[2];
                    card.setcard = data[3];
                    card.type = data[4];
                    card.atk = data[5];
                    card.def = data[6];
                    card.level = data[7][0];
                    card.pendulum = data[7][1];
                    card.race = data[8];
                    card.attribute = data[9];
                    card.category = data[10];
                    card.origin_name = data[12];
                    card.name = data[12];
                    card.desc = data[13];
                    card.hint = data[14];
                    card.pic = data[15];
                    card.center_pic = data[16];
                    card_change.get_all();
                } catch (error) {}
            } as () => Promise<void>,
            paste : async function(i) {
                try {
                    let response = await axios.post(`${window.location.href}api/save_cdb`, {
                        data: copy.content[i][0],
                        code: copy.content[i][1],
                        cdb: open.cdb
                    });
                } catch (error) {}
            } as (i : number) => Promise<void>,
            save : async function(chk) {
                if (select.id <= 0) return;
                try {
                    emit.pic_page.download_pic.to();
                    let response = await axios.post(`${window.location.href}api/save_cdb`, {
                        data: [
                            card_n.id,
                            card_n.ot,
                            card_n.alias,
                            card_n.setcard,
                            card_n.type,
                            card_n.atk,
                            card_n.def,
                            card_n.level,
                            card_n.race,
                            card_n.attribute,
                            card_n.category,
                            card_n.id,
                            card.name,
                            card.desc
                        ].concat(card.hint),
                        code: card.origin_id,
                        cdb: open.cdb
                    });
                    if (chk != 'add' && response.data == 'removed') {
                        emit.list_page.cdb_changed.to();
                    }
                } catch (error) {}
            } as (chk ?: string) => Promise<void>,
            add : async function() {
                let id = -1;
                try {
                    let response = await axios.post(`${window.location.href}api/add_cdb`, {
                        cdb: open.cdb
                    });
                    id = response.data;
                } catch (error) {}
                return id;
            } as () => Promise<number>,
            del : async function() {
                try {
                    let response = await axios.post(`${window.location.href}api/del_cdb`, {
                        code: card.origin_id,
                        cdb: open.cdb
                    });
                } catch (error) {}
            } as () => Promise<void>
        }
    });

    let card_n = reactive({
        id : 0,
        alias : 0,
        ot : 0,
        level : 0,
        atk : 0,
        def : 0,
        setcard : 0,
        race : 0,
        attribute : 0,
        type : 0,
        category : 0,
        setcard_name : Array(4).fill('')
    });

    let vif = reactive({
        show : {
            category : {
                chk : false,
                title : '效果分类'
            },
            type : {
                chk : false,
                title : '卡片类型'
            },
            hint : {
                chk : false,
                title : '提示文字'
            },
            pic : {
                chk : true,
                title : '卡图设置'
            },
            link : {
                chk : true,
                title : '点击隐藏连接箭头',
                content : '&#10003'
            },
            pic_cut : {
                chk : false,
                cut_or_set : false
            }
        },
        is_type : {
            link : false,
            pendulum : false
        },
        warn : {
            same_id : false,
            id : ''
        }
    });

    let copy = reactive({
        content : [],
        from : async function() {
            if (card.origin_id <= 0 || card_n.id >= 100000000 || card_n.id == 0) {
                if (card.origin_id <= 0)
                    window.alert('请先选择卡片');
                else window.alert('请先定义卡号');
                return;
            }
            await card.data.save();
            copy.content = [[
                [
                    card_n.id,
                    card_n.ot,
                    card_n.alias,
                    card_n.setcard,
                    card_n.type,
                    card_n.atk,
                    card_n.def,
                    card_n.level,
                    card_n.race,
                    card_n.attribute,
                    card_n.category,
                    card_n.id,
                    card.name,
                    card.desc
                ].concat(card.hint),
                card.origin_id,
                open.cdb,
            ]];
            window.alert('已复制:   ' + card.id + ' ' + card.name);
        } as () => void,
        to : async function() {
            if (copy.content.length == 0 || open.cdb == '') {
                window.alert('请先复制');
                return;
            }
            let same_group = [];
            for (let i = 0; i < copy.content.length; i++)
                if (open.list.flat().filter(e => e.split(' ')[0] == copy.content[i][0][0]).length > 0)
                    same_group.push(copy.content[i][0][0] + ' ' + copy.content[i][0][12]);
            if (same_group.length > 0 && !window.confirm('存在卡片冲突，是否仍要复制？\n' + same_group)) return;
            for (let i = 0; i < copy.content.length; i++)
                await card.data.paste(i);
            await card.data.save();
            emit.list_page.cdb_changed.to(copy.content[0][1]);
            copy.content = [];
        } as () => void
    });

    let pic_setting = reactive({
        package : '',
        descriptionZoom : 1,
        descriptionWeight : 0,
        descriptionAlign : false,
        firstLineCompress : false,
        copyright : '',
        laser : '',
        rare : '',
        radius : true
    });

    let upload_file_input = ref(null);
    let upload_file = {
        url : '',
        uploading : false,
        resert : function() {
            URL.revokeObjectURL(upload_file.url);
            upload_file.url = '';
        },
        click : async function (e) {
            if (select.id <= 0) {
                e.target.value = '';
                return;
            }
            try {
                let files = e.target.files;
                if (files.length > 0) {
                    let file = files[0];
                    if (file.type.includes('image')) {
                        upload_file.url = URL.createObjectURL(file);
                        await (new Promise(resolve => setTimeout(resolve, 5)));
                        emit.pic_cut_page.upload.to(upload_file.url);
                    }
                }
                e.target.value = '';
            } catch (error) { console.error(error); }
        } as (e: any) => Promise<void>,
        drag : async function (e) {
            if (select.id <= 0) return;
            let files = e.dataTransfer.files;
            if (files.length > 0) {
                let file = files[0];
                if (file.type.includes('image')) {
                    upload_file.url = URL.createObjectURL(file);
                    await (new Promise(resolve => setTimeout(resolve, 5)));
                    emit.pic_cut_page.upload.to(upload_file.url);
                }
            }
            upload_file.uploading = false;
        } as (e: any) => Promise<void>,
        send : async function (formData) {
            try {
                let response = await axios.post(`${window.location.href}api/get_center_pic`, formData);
                card.center_pic = response.data;
            } catch (error) {}
        } as (formData: FormData) => Promise<void>
    }

    let card_change = {
        get_all : function() {
            for (let i = 0; i < 4; i++) {
                card_change.setcard(i);
                card_change.setcard_name(i);
            }
            for (let i = 0; i < lists.type.length; i++) {
                card_change.type(i);
            }
            for (let i = 0; i < lists.category.length; i++) {
                card_change.category(i);
            }
        } as () => void,
        setcard : function(i) {
            // card_n.setcard_name[i] = lists.setcard.find(e => e[0] == card.setcard[i])?.[1] as string ?? (lists.custom_setcard.find(e => e[0] == card.setcard[i])?.[1] as string ?? '');
            // card_n.setcard = parseInt(card.setcard.slice().sort((a, b) => parseInt(a, 16) - parseInt(b, 16)).map(e => ('0'.repeat(4 - e.slice(0, 4).length)) + e.slice(0, 4)).join(''), 16);
        } as (i: number) => void,
        setcard_name : function(i) {
            // if (card.setcard[i] == 0 || lists.setcard.find(e => e[0] == card.setcard[i])) return;
            // let r = lists.custom_setcard.find(e => e[0] == card.setcard[i]);
            // r ? r[1] = card_n.setcard_name[i] : lists.custom_setcard.push([card.setcard[i], card_n.setcard_name[i]]);
        } as (i: number) => void,
        atk : function() {
            card_n.atk = card.atk != '?' ? card.atk as number : -2; 
        } as () => void,
        def : function() {
            card_n.def = (card_n.type & 0x4000000) == 0 ? (card.def != '?' ? card.def as number : -2) : card.link; 
        } as () => void,
        name : function() {
            emit.list_page.card_changed.to(vif.warn.same_id ? card.origin_id : card.id, card.name);
        } as () => void,
        id : function() {
            console.log(card.id);
            if (open.list.flat().filter(e => e.split(' ')[0] == card.id).length > 0 && card.origin_id != card.id) {
                vif.warn.same_id = true;
                if (select.id > 0)
                    emit.list_page.card_changed.to(card.origin_id, card.name);
            } else {
                if (vif.warn.same_id)
                    vif.warn.same_id = false;
                if (select.id > 0)
                    emit.list_page.card_changed.to(card.id, card.name);
            }
            card_n.id = (vif.warn.same_id || card.id.toString().length == 0 || card.id == 0 ? (card.origin_id > 10000000000 ? 0 : card.origin_id) : card.id);
        } as () => void,
        alias : function() {
            card_n.alias = (card.alias.toString().length == 0 ? 0 : card.alias);
        } as () => void,
        ot : function() {
            card_n.ot = lists.ot.find(e => e[1] == card.ot)?.[0] as number ?? 0;
        } as () => void,
        level : function() {
            card_n.level = lists.level.find(e => e[1] == card.level)?.[0] as number ?? 0;
            if (vif.is_type.pendulum) {
                card_n.level |= (card.pendulum << 16);
                card_n.level |= (card.pendulum << 24);
            }
        } as () => void,
        race : function () {
            card_n.race = lists.race.find(e => e[1] == card.race)?.[0] as number ?? 0;
        } as () => void,
        attribute : function() {
            card_n.attribute = lists.attribute.find(e => e[1] == card.attribute)?.[0] as number ?? 0;
        } as () => void,
        type : function(i) {
            card.type[i] ? card_n.type |= lists.type[i][0] : card_n.type &= ~lists.type[i][0];
            vif.is_type.pendulum = (card_n.type & 0x1000000) > 0;
            vif.is_type.link = (card_n.type & 0x4000000) > 0;
        } as (i: number) => void,
        category : function(i) {
            card.category[i] ? card_n.category |= lists.category[i][0] : card_n.category &= ~lists.category[i][0];
        } as (i: number) => void,
    };

    onBeforeMount(() => {
        for (let i = 1; i < 9; i++) {
            if (i == 5) {
                lists.link_pics.push('');
            }
            lists.link_pics.push('./link-arrow/arrow-' + i + '-off.png');
        }
        lists.get();
        card.clear();
    });

    watch(card, async (n) => {
        await (new Promise(resolve => setTimeout(resolve, 5)));
        n.pic == '' ? emit.pic_page.load_pic.to() : emit.pic_page.unload_pic.to();
    }, { deep: true });

    watch (() => card.id, () => { card_change.id(); });
    watch (() => card.name, () => { card_change.name(); });
    watch (() => card.atk, () => { card_change.atk(); });
    watch (() => card.def, () => { card_change.def(); });
    watch (() => card.alias, () => { card_change.alias(); });
    watch (() => card.ot, () => { card_change.ot(); });
    watch (() => card.level, () => { card_change.level(); });
    watch (() => card.race, () => { card_change.race(); });
    watch (() => card.attribute, () => { card_change.attribute(); });

    watch(pic_setting, () => {
        if (card.pic == '')
            emit.pic_page.load_pic.to();
        else
            emit.pic_page.unload_pic.to();
    }, { deep: true });

    let open = reactive({
        cdb : '',
        list : []
    });

    let select = reactive({
        id : -1
    });

    let em = defineEmits(['event_create_new_cdb', 'event_remove_cdb'])

    let emit = {
        main_page : {
            cdb_closed : {
                on : function() {
                    card.data.save();
                    card.clear();
                    open.cdb = '';
                    open.list = [];
                } as () => void,
                to : function() {
                    em('event_remove_cdb', open.cdb);
                } as () => void
            },
            cdb_opened  : {
                on : function(cdb) {
                    open.cdb = cdb[0][0];
                    open.list = cdb;
                } as () => void
            },
            cdb_add : {
                to : function() {
                    em('event_create_new_cdb');
                } as () => void
            }
        },
        list_page : {
            select_card : {
                on : async function (i : Map<string, any> = new Map().set('id', -1)) {
                    await card.data.save();
                    select.id = i.get('id');

                    if (select.id < 0)
                        card.clear();
                    else
                        await card.data.get();

                    emit.list_page.get_over.to();
                } as (i : Map<string, any>) => Promise<void>
            },
            card_changed : {
                to : function (id, name) {
                    emitter.emit('to_lpage_card_changed', id.toString() + ' ' + name);
                } as (id: number, name: string) => void
            },
            cdb_changed : {
                to : function (id = -1) {
                    emitter.emit('to_lpage_cdb_changed', id);
                } as (id ?: number) => void,
                on : function (cdb) {
                    open.list = cdb;
                } as (cdb: any[]) => void
            },
            get_over : {
                to : function() {
                    emitter.emit('to_lpage_get_over');
                }
            },
            search : {
                to : function(str) {
                    emitter.emit('to_lpage_search', str);
                } as (str: any[]) => void
            }
        },
        download_page : {
            save : {
                on : async function() {
                    await card.data.save();
                    emit.download_page.save.to();
                } as () => Promise<void>,
                to : function() {
                    emitter.emit('to_dpage_save');
                } as () => void
            }
        },
        pic_page : {
            unload_pic : {
                to : function() {
                    emitter.emit('to_ppage_unload_pic');
                } as () => void
            },
            load_pic : {
                to : function() {
                    emitter.emit('to_ppage_load_pic', new Map().set('card', card).set('card_n', card_n).set('list', lists.type.slice()).set('pic', pic_setting).set('open', open.cdb));
                } as () => void
            },
            download_pic : {
                to : function() {
                    emitter.emit('to_ppage_download_pic', new Map().set('card', card).set('card_n', card_n).set('list', lists.type.slice()).set('pic', pic_setting).set('open', open.cdb));
                } as () => void
            }
        },
        pic_cut_page : {
            upload : {
                to : function(url) {
                    emitter.emit('to_pcpage_upload', new Map().set('url', url).set('id', card.origin_id));
                } as (url: string) => void,
                on : function(file) {
                    let formData = new FormData();
                    formData.append('file', file);
                    URL.revokeObjectURL(upload_file.url);
                    upload_file.url = '';
                    upload_file.send(formData);
                } as (file: File) => void
            }
        }
    }

    emitter.on('to_cpage_cdb_closed', emit.main_page.cdb_closed.on);
    emitter.on('to_cpage_cdb_opened', emit.main_page.cdb_opened.on);
    emitter.on('to_cpage_cdb_changed', emit.list_page.cdb_changed.on);
    emitter.on('to_cpage_send_select', emit.list_page.select_card.on);
    emitter.on('to_cpage_save', emit.download_page.save.on);
    emitter.on('to_cpage_upload', emit.pic_cut_page.upload.on);

    function filter_input(event, t, str_filter = /[^0-9]/) {
        let input_value = event.target.value;
        let new_value = input_value.replace(str_filter, '')
        switch (t[0]) {
            case'card_setcard':
                card.setcard[t[1]] = new_value.slice(0, 4);
                break;
            case 'card_id':
                card.id = new_value.slice(0, 9);
                break;
            case 'card_alias':
                card.alias = new_value.slice(0, 9);
                break;
            case 'card_atk':
                if (input_value.slice(0, 1) == '-' || input_value.slice(0, 1) == '?') {
                    card.atk = '?';
                } else {
                    card.atk = new_value.slice(0, 19);
                }
                break;
            case 'card_def':
                if (input_value.slice(0, 1) == '-' || input_value.slice(0, 1) == '?') {
                    card.def = '?';
                } else {
                    card.def = new_value.slice(0, 19);
                }
                break;
            case 'card_pendulum':
                while (new_value != '' && parseInt(new_value) > 15)
                    new_value = new_value.slice(0, -1);
                card.pendulum = new_value;
                break;
        }
    }

    async function whether_show_rpage(v) {
        if (vif.show.category.chk && v == 'category') return;
        if (vif.show.type.chk && v == 'type') return;
        if (vif.show.hint.chk && v == 'hint') return;
        if (vif.show.pic.chk && v == 'pic') return;
        vif.show.category.chk = false;
        vif.show.type.chk = false;
        vif.show.hint.chk = false;
        vif.show.pic.chk = false;
        await(new Promise(resolve => setTimeout(resolve, 400)));
        switch (v) {
            case 'category':
                vif.show.category.chk = true;
                break;
            case 'type':
                vif.show.type.chk = true;
                break;
            case 'hint':
                vif.show.hint.chk = true;
                break;
            case 'pic':
                vif.show.pic.chk = true;
                break;
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

    #card_id , #card_atk{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(3, 1fr);
    }

    #card_id input, #card_atk input {
        grid-column-start: 2;
        grid-column-end: 4;
        width: 80%;
    }

    #card_id strong {
        color: red;
        grid-column-start: 1;
        grid-column-end: 4;
    }

    #card_setcard {
        width: 100%;
        grid-row-gap: 0.5vh;
        display: grid;
        grid-template-rows: repeat(4, 1fr);
        align-items: center;
        justify-items: center;
    }

    #card_setcard div {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
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

    #card_pic img, .pic {
        max-width: 17.5vw;
        height: 110%;
        width: auto;
        display: block;
    }

    #card_link img {
        height: 100%;
        width: 100%;
    }

    #card_right {
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

        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(16, 1fr);

        justify-items: left;
    }

    #card_category div, #card_type div {
        width: 100%;

        display: grid;
        grid-template-columns: repeat(3, 1fr);
    }

    #card_category div span, #card_type div span {
        grid-column-start: 1;
        grid-column-end: 3;
        justify-self: center;
        align-self: center;
    }

    #card_category div input, #card_type div input {
        grid-column-start: 3;
        grid-column-end: 4;
        justify-self: right;
        align-self: center;

        height: 50%;
        width: 50%;
    }

    .change_rpage_btn {
        align-self: center;
        justify-self: right;

        grid-row-start: 1;
        grid-row-end: 2;
    }

    #card_hint, #card_pic_setting {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-template-rows: repeat(17, 1fr);

        align-items: center;
    }

    #card_type, #card_category, #card_hint, #card_pic_setting {
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

    .card_pic_setting_content {
        grid-column-start: 1;
        grid-column-end: 5;
        grid-row-start: 3;
        grid-row-end: 18;

        display: grid;
        grid-template-columns: repeat(3, 1fr);
        grid-template-rows: repeat(16, 1fr);

        height: 100%;
    }

    .card_pic_setting_content span {
        grid-column-start: 1;
        grid-column-end: 2;
    }

    #card_box_btn {
        grid-column-start: 1;
        grid-column-end: 3;
        grid-row-start: 16;
        grid-row-end: 17;

        width: 100%;

        display: flex;
        justify-content: center;
    }

    #upload_area {
        width: 80%;
        height: 90%;
        border: 2px dashed #bbbbbb;
        color: #bbbbbb;

        justify-self: center;
        text-align: center;

        cursor: pointer;
    }

    #upload_area:hover {
        border: 2px dashed black;
        color: black;
    }

    .card_right-enter-active,
    .card_right-leave-active {
        transition: opacity 0.5s ease;
    }

    .card_right-enter-from,
    .card_right-leave-to {
        opacity: 0;
    }

    .card_right-enter-to,
    .card_right-leave-from {
        opacity: 1;
    }
</style>