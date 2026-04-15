a todo list 
====

https://gemini.google.com/u/1/app/ebf934568093772e  分析

https://gemini.google.com/u/1/app/e97b40199ca7ef46 架构



copy from hugo do it version v0.4.0 

# other file 参考
MarkDown/2023-01-07_golang_learn_note.md
MarkDown/2022-09-20_lua将user表和jump表分开.md
MarkDown/2023-02-10_HUGO_静态网站_cookies_共享.md
https://www.fusejs.io/examples.html#search-string-array


# todo list steps
- [x] 找一找之前自己做的东西, 里面有没有记录自己怎么搞这个 主题的
- [x] 自己改的所有的东西,都记下来
- [x] make a getit.cc website 
    - [x] install hugo on macbook 
        - [x] try brew install method 
            - try : brew install hugo-extended  
                - [x] 没找到 hugo-extended
            - [x] try :brew install hugo 
                - hugo v0.120.4-f11bca5fec2ebb3a02727fb2a5cfb08da96fd9df+extended
                - 似乎包含了 extended
        - [x] install the 直接安装满足你操作系统 (Windows, Linux, macOS) 的最新版本  Hugo (> 0.83.0). 
        - [x] hugo version must > 0.83.0 
        - [x] 由于这个主题的一些特性需要将  SCSS 转换为  CSS, 推荐使用 Hugo extended 版本来获得更好的使用体验. 
        - [x] hugo version better is : hugo extended
    - [x] try make some md file
        - [x] export from game.cc?
        - [x] try upload some img file to imgcdn.cc ; ok 
- [x] how hugo know which theme used ?
    - [x] how? use the hugo.toml 
- [x] clear game.cc website 
    - [x] reclone github getit theme 
- [x] 获取 github 里面 doit的最新的 release版. 
    - [x] 在此版本的基础上, 自建一hugo个分支: getit
    - [x] 首页弄成 多样式的那种, 研究一下是怎么做到的.
- [x] try update raspberry pi hugo version to 120 
    - move hugo /usr/bin/hugo

- [x] make a website with at last 12 posts md file 
    - [x] export the md file from game.cc ,cool !
    - [x] then make the website . 
    - [x] then edit the theme 

- [x] the hugo_getit , check the different codes 
    - [x] make a new copy 
    - [x] upload a new load 
    - [x] i remember i used the last version . 
    - [x] I find it : Add suport giscus comment system  
    - [x] between : Commits on Nov 4, 2021   -   Commits on Nov 6, 2021
    - [x] find it :
        - chore: add 0.2.13 changelog     Nov 6, 2021   ## [0.2.13] - 2021-11-06
- [x] check the different with doit getit 
- [x] try to see how meili search work
- [x] built website with doit v0.4
    - [x] install nginx on macos ? ?
        - [x] raspberry is better ? Yes , it's better . 
        - [x] but nginx ?? on macos, better to 
        - [x] or install caddy2 ?
            - [x] yeap ,instal caddy2 on macos ,is better! 
    - [x] move git folder to raspberry pi . 
    - [x] move hugo folder to raspberry pi folder 

- [x] homepage auto adapts to screens 
    - [x] copy from getit old version .
    - [x] try use hugo , caddy2 
    - [x] change the first page url 
    - [x] try edit the hoem page , and adjust it 

- [x] edit home page , adjust 
    - [x] card summary 
    - [x] img size
    - [x] screen size 

- [x] try edit fuse , and index.json creat 
    - [x] try use list 

- [x] hugo filename ? how ? chinese words

- [x] use less control the login page 

- [x] edit about page to a new 
    - [x] how about page creat ?
        - [x] If need content , add the content 
        - [x] need the content 
- [x] add pages : 
    - [x] user/  need md 
        - [x] use type ? cools , page ?  Or anything else ?
        - [x] add html 
        - [x] add css 
    - [x] login/ no md 
        - [x] add html 
        - [x] add scss 

- [x] add a info page 

- [x] BUG: the first click search bug ,the print not on the search arear.

- [x] nginx lua redis , 
    - [x] how import redis ?
    - [x] use which redis component
        - [x] lua resty redis 

- [x] 测试 ngx.say后面的代码是否还会执行
    - [x] 需要一个 ngx.exit
    - [x] 测试一下就知道了. 没结束.果然没结束. 多个say可以逐个输出. 需要加 ngx.exit

- [x] nginx重定向 ngx.redirect 后面的代码会执行吗
    - 不会执行. 

- [x] ngx.cookie_time(time) return a cookie time 

- [x] token add a unix time ? no!


- [x] try get user info 
    - [x] cookie ,only token 

- [] js web storage invite code .  cool way 

- [x] lua 代码规范
    - 文件: 小写 下划线
    - 空行
        - 函数之间加
        - 函数内,逻辑紧密的语句间不加 
    - 类, 函数: 大驼峰
    - 变量 : 小驼峰
    - 常量 全大写 + _
    - 临时变量 _ _xxx i k v t 

- [x] cookie 
    - token only 
    - inviteby 

- [x] lua shared dict 
    - token token_

- [x] 约定的 api 规则
    - /user
        - /user/login  post 
            - email=xx&pwd=xx
            - ok,userid
                - cookie set session/token
        - /user/reg  post 
            - name=xx&email=xx&pwd=xx&invite_by=xx
            - ok,userid
                - cookie set token /session
        - /user/info   post 
            - session=xx
            - ok,userinfo
    - /url
        - /url?id=xxx  get cookie
    - /admin
        - /urls  post token=xxx&urls={}   urls:{} obj

- [x] 约定的数据传输方式
    - url args 
    - name=xxx&id=xx&gaa=xx&email=xx ...

- [x] lua files :
    - user.lua
    - admin.lua
    - url.lua

- [x] db:  with site pre .   site prefix = 'g_'
    - pre_user_email  hash  many ; user info hash 
        - id
        - name 
        - email 
        - pwd
        - coins money  1$=100coin 
        - urlclicks
        - ip 
        - ipv6 
        - divices
        - inviteby 
        - invites 
    - pre_users_index   set 
    - pre_urls   hash  one 
    - pre_invite_codes_index   hash  one  
    - pre_invites_list_email  set many  ; user invite user list 
    - pre_all_users_count : string number , incresment

- [x] ngx shared dict :
    - pre_reg_ip_ip

- [x] try understand the hugo themes reasons 

- [x] add the home page cards spacing . make it wider .

- [x] learn the theme 
    - first : alyouts : index.html ,  add a  summary-card , 
    - assets css _page _home.scss , add a  summary-card , css 
    - then the _media.scss 

- [x] js window.location.search  , if no ? , 
```html 
<script>
    var inviteby = window.location.search;
    if (inviteby ) {
        console.log(inviteby)
    }   
    
</script>
```

- [x] the fucking redis:hget ?  userdata????
    - [x] ngx.null   ??? waht f**k ,  nil !!!
    - [x] nil : redis error 
    - [x] null : redis : null !  so fuk

- [x] why I remake a getit theme ?
    - [x] Need make the steps , how I make it possible 

- [x] the invite code set on index page ? 

- [x] hugo theme doit theme , edit
	- [x] get github hugo getit 

- [x] value of redis can not be null !

- [x] make a copy to raspiberry pi , try use the live mode 

- [x] home page UI adaptive size 
    - [x] refer to  love it theme 


- [x] fuse.js use list to search 
    - [x] the search , only  title . is OK  save the json file size .

- [x] the urldecode  infopage 

- [x] fuck safari : 防止跨站跟踪!  
    - the same top domain , safari ok!
    - 如果需要在safari浏览器中使用, site 和 jump的domain,必须是同一个二级域名. 不然的话,会导致跨站的问题

- [x] fuse.mini:
    - posts: 4944 
    - index.json: 161kb
    - idnex.json gzip : 93.06kb
    - COOL!

- [] js check http or https ? auto https 
    - [] 
    var protocolStr = document.location.protocol;
    if(protocolStr == "http:")
    {
    console.log("protocol = " + protocolStr);
    }
    else if(protocolStr == "https:")
    {
    console.log("protocol = " + protocolStr);
    }
    else
    {
    console.log("other protocol");
    }
- [] edit the user page 

- [] login page ,add a invite code input button

- [] use artalk as backend .
    - [] install artalk 

- [] python script 

- [] in future , consider meilisearch !
    - [] the fast and powerful search ! 

- [] lua实现模糊查询
    - [] ngx.re.find , 然后把标题,时间,url 放到一个文件中去,逐行对比

- [] redis 实现查询: 
    - 插件 redisearch 

- [] 开源搜索引擎:  meilisearch  zincsearch redisearch


- [] api 变为:  go.lua , vip.lua, admin.lua ,
