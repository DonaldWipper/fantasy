(window.webpackJsonp = window.webpackJsonp || []).push([
    [19], {
        "5yIE": function(t, e, n) {
            (function(a) {
                var i, s;
                i = [n("3a3M"), n("1NHe"), n("3A4U"), n("di0A"), n("Xx+T"), n("DGju")], void 0 === (s = function(t, e, n, i, s, o) {
                    "use strict";
                    var r = {};

                    function l() {
                        e.apply(this, arguments)
                    }
                    return r.replaceOldAuthBlock = function() {
                        var e = document.querySelector('.overlay-popup[data-control="Common.Authorization"]'),
                            n = document.querySelector('.overlay-popup[data-control="Common.Registration"]');
                        e && e.remove(), n && n.remove(), document.body.insertAdjacentHTML("afterbegin", s["_desktop/common/views/auth/auth"]({
                            request_env: window.Sports.request_env,
                            is_old_static: !o.default
                        })), t('.popup__overlay[data-control="Common.Auth"]').view("Common.Auth"), t('.popup__overlay[data-control="Common.Auth"]').auto()
                    }, o.default ? (window.Sports = window.Sports || {}, window.Sports.q = window.Sports.q || [], window.Sports.q.push(r.replaceOldAuthBlock)) : r.replaceOldAuthBlock(), r.initCaptcha = function() {
                        return new a((function(t, e) {
                            var n = document.createElement("script");
                            
                            
                            window.SportsGrecaptchaLoaded = function() {
                                t()
                            }, n.src = "https://www.google.com/recaptcha/api.js?onload=SportsGrecaptchaLoaded&render=explicit", document.head.appendChild(n), n.onerror = e
                        }))
                    }, l.prototype = Object.create(e.prototype), l.prototype.initialize = function() {
                        if (e.prototype.initialize.apply(this, arguments), this.grecaptchaWidgetId = null, this.$tabs = this.$element.find(r.selectors.tabs), this.$btn = this.$element.find(r.selectors.btn), this.$statusError = this.$element.find(r.selectors.statusError), this.$statusSuccess = this.$element.find(r.selectors.statusSuccess), this.redirect = this.$element.data("redirect"), !this.redirect || !this.redirect.length) {
                            var t = i.getArgument("url");
                            t.isSet ? this.redirect = t.value : window.location.href.indexOf("/login/") > -1 && (this.redirect = "/")
                        }
                        return this
                    }, l.prototype.listen = function() {
                        var t = this;
                        return e.prototype.listen.apply(this, arguments), this.$element.on("submit", r.selectors.authForm, this.login.bind(this)).on("submit", r.selectors.remindForm, this.remind.bind(this)).on("submit", r.selectors.regForm, this.register.bind(this)).on("click", r.selectors.btnRemind, this.eventForgotPassword.bind(this)).on("click", r.selectors.btnLogin, this.eventTabTopLogin.bind(this)).on("click", r.selectors.btnReg, this.eventOpenRegistration.bind(this)), n.instance().on("login:complete login:progress login:fail registration:fail", this.loginStatus.bind(this)).on("remind:complete remind:fail", this.remindStatus.bind(this)), this.on("opened-auth", (function(e) {
                            t.getRecaptchaWidgetId(e)
                        })), this
                    }, l.prototype.render = function() {
                        return e.prototype.render.apply(this, arguments), this
                    }, l.prototype.login = function(e) {
                        var a = this;
                        if (e.preventDefault(), this.disabled) return !1;
                        this.stateLoading(!0);
                        var i = this.data(t(e.currentTarget));
                        return this.getRecaptchaWidgetId("login").then((function() {
                            a.updateCaptcha().then((function(t) {
                                i["g-recaptcha-response"] = t, n.instance().set("social", "local").login(i)
                            }))
                        })).catch((function(t) {
                            throw new Error("[SPORTS][Auth-block]: authorization error", t)
                        })), this
                    }, l.prototype.updateCaptcha = function() {
                        var t = this;
                        return new a((function(e, n) {
                            t.on("recaptcha:response", (function(n) {
                                t.off("recaptcha:response"), e(n)
                            })), grecaptcha.reset(t.grecaptchaWidgetId), grecaptcha.execute(t.grecaptchaWidgetId), setTimeout((function() {
                                var t = document.querySelector('iframe[src^="https://www.google.com/recaptcha/api2/bframe"]');
                                t && (t.parentNode.style.position = "fixed", t.parentNode.style.top = "50%", t.parentNode.style.transform = "translateY(-50%)")
                            }), 3e3)
                        }))
                    }, l.prototype.register = function(e) {
                        var a, i = this;
                        if (e.preventDefault(), this.disabled) return !1;
                        this.stateLoading.call(this, !0);
                        var s = this.data(t(e.currentTarget));
                        return this.getRecaptchaWidgetId("register").then((function() {
                            i.updateCaptcha().then((function(t) {
                                s["g-recaptcha-response"] = t, !0 === (a = i.passwordIdentity(s))[0] ? n.instance().set("social", "local").register(s) : n.instance().trigger("registration:fail", -2, a)
                            }))
                        })), this
                    }, l.prototype.remind = function(e) {
                        return e.preventDefault(), !this.disabled && (this.stateLoading.call(this, !0), n.instance().set("social", "local").remind(this.data(t(e.currentTarget))), this)
                    }, l.prototype.loginStatus = function(e, a) {
                        if (this.stateLoading.call(this, !1), 1 === e) "local" != n.instance().get("social") && n.instance().register(t.extend(a, {
                            remember_me: 1
                        }));
                        else if (e < 0) return this.showStatus("error", a), grecaptcha.reset(this.grecaptchaWidgetId), this;
                        return e >= 0 && (this.close(), this.redirect ? window.location.href = decodeURIComponent(this.redirect) : window.location.reload(!0)), this
                    }, l.prototype.remindStatus = function(t, e) {
                        return "success" == (t = t < 0 ? "error" : "success") && (this.$element.find(r.selectors.authForm + " " + r.selectors.inputEmail).val(this.$element.find(r.selectors.remindForm + " " + r.selectors.inputEmail).val()), setTimeout(function() {
                            this.setTab(0, !0)
                        }.bind(this), 3e3)), this.stateLoading.call(this, !1), this.showStatus(t, e), this
                    }, l.prototype.stateLoading = function(t) {
                        t ? (this.disabled = !0, this.$btn.addClass(r.modifiers.loading)) : setTimeout(function() {
                            this.disabled = !1, this.$btn.removeClass(r.modifiers.loading)
                        }.bind(this), 200)
                    }, l.prototype.passwordIdentity = function(t) {
                        var e = [];
                        return t.password === t.repasswd ? e[0] = !0 : e[0] = {
                            code: "UnequalPasswords",
                            message: "Не совпадают поля паролей"
                        }, e
                    }, l.prototype.showStatus = function(t, e) {
                        var n;
                        this.timeout && this.clearStatus.call(this), n = e && e.length ? e[0].message || e[0] : "error" === t ? "Ошибка" : "", "error" === t ? this.$statusError.html(n) : this.$statusSuccess.html(n), this.timeout = setTimeout(this.clearStatus.bind(this), 3e3)
                    }, l.prototype.clearStatus = function() {
                        clearTimeout(this.timeout), this.timeout = null, this.$statusError.html(""), this.$statusSuccess.html("")
                    }, l.prototype.eventForgotPassword = function(t) {
                        t && t.preventDefault(), this.setTab(2, !1), this.clearStatus.call(this)
                    }, l.prototype.eventTabTopLogin = function(t) {
                        t && t.preventDefault(), this.setTab(0, !0), this.clearStatus.call(this)
                    }, l.prototype.eventOpenRegistration = function(t) {
                        t && t.preventDefault(), this.setTab(1, !0), this.clearStatus.call(this)
                    }, l.prototype.data = function(t) {
                        var e, n, a, i, s;
                        for (n = {}, a = 0, i = (s = t.serializeArray()).length; a < i; a++) n[(e = s[a]).name] = e.value;
                        return n
                    }, l.prototype.getRecaptchaWidgetId = function(t) {
                        var e = this;
                        return null !== this.grecaptchaWidgetId || "login" != t && "register" != t ? new a((function(t, n) {
                            return t(e.grecaptchaWidgetId)
                        })) : r.initCaptcha().then((function() {
                            e.grecaptchaWidgetId = grecaptcha.render(e.element.querySelector(r.selectors.captchaContainer), {
                               
                                sitekey: "6LfctWkUAAAAAA0IBo4Q7wlWetU0jcVC7v5BXbFT",
                                isolated: !0,
                                callback: function(t) {
                                    return e.trigger("recaptcha:response", t)
                                }
                            })
                        })).catch((function(t) {
                            console.error("[SPORTS][AuthBlock]: Error in captcha loading", t)
                        }))
                    }, l.prototype.setTab = function(t, e) {
                        var n = o.default ? this.$tabs.view("Common.Tabs") : this.$tabs.view("Common.NewTabs");
                        n.then ? n.then((function(n) {
                            n.open(t, e)
                        })) : n.data("sports:control").open(t, e)
                    }, r.selectors = {
                        inputEmail: ".auth__login-input_email",
                        authForm: ".auth__login",
                        regForm: ".auth__reg",
                        remindForm: ".auth__remind",
                        tabs: ".auth__tabs",
                        forgotPassword: ".auth__forgot-password",
                        btnLogin: ".auth__btn-login",
                        btnRemind: ".auth__btn-remind",
                        btnReg: ".auth_reg-link",
                        btn: ".auth__btn",
                        statusError: ".auth__message-error",
                        statusSuccess: ".auth__message-success",
                        captchaContainer: ".js-captcha-container"
                    }, r.modifiers = {
                        open: "modal_state_open",
                        loading: "loader-gray_state_active"
                    }, l
                }.apply(e, i)) || (t.exports = s)
            }).call(this, n("DDJD"))
        },
        G8mn: function(t, e, n) {
            var a = n("Fanx");

            function i(t) {
                return t && (t.__esModule ? t.default : t)
            }
            t.exports = (a.default || a).template({
                1: function(t, e, n, a) {
                    return "Sports.ru?"
                },
                3: function(t, e, a, s) {
                    var o;
                    return null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "cyber.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(4, s, 0),
                        inverse: this.program(6, s, 0),
                        data: s
                    })) ? o : ""
                },
                4: function(t, e, n, a) {
                    return "cyber.sports.ru?"
                },
                6: function(t, e, n, a) {
                    return "Tribuna.com?"
                },
                compiler: [6, ">= 2.0.0-beta.1"],
                main: function(t, e, a, s) {
                    var o;
                    return '<div class="auth__content clearfix">\n    <form class="auth__remind">\n        <div class="auth__title">Восстановление пароля</div>\n        <div class="auth__form-row auth__remind-form-row">\n            <label>\n                <input class="auth__login-input auth__login-input_email input input_size_extra-large" type="text" name="login" placeholder="Ваш e-mail">\n            </label>\n            <a class="auth__forgot-password auth__btn-login link link_color_gray link_size_tiny" href="#" rel="nofollow">Отменить</a>\n        </div>\n        <div class="auth__form-row">\n            <button class="btn btn_color_black-light btn_size_extra-large auth__btn auth__login-btn loader-gray" type="submit">Сбросить пароль</button>\n            <div class="auth__message">\n                <span class="auth__message-error"></span>\n                <span class="auth__message-success"></span>\n            </div>\n\n        </div>\n        <input type="hidden" name="back_url" value="/logon.html">\n    </form>\n    <p class="auth__bottom-text">\n        Еще не зарегистрированы на ' + (null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "www.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(1, s, 0),
                        inverse: this.program(3, s, 0),
                        data: s
                    })) ? o : "") + '<br>\n        <a class="auth_reg-link link link_color_blue" href="#" rel="nofollow">Зарегистрироваться</a>\n    </p>\n</div>\n'
                },
                useData: !0
            })
        },
        JgMM: function(t, e, n) {
            "use strict";
            n("jZI0");
            var a, i = (a = n("r6CY")) && a.__esModule ? a : {
                default: a
            };
            t.exports = i.default
        },
        Ogd4: function(t, e, n) {
            var a, i;
            a = [n("3a3M"), n("1NHe"), n("MgL6"), n("di0A")], void 0 === (i = function(t, e, n, a) {
                "use strict";
                var i = {};

                function s() {
                    e.apply(this, arguments)
                }
                return s.prototype = Object.create(e.prototype), s.prototype.initialize = function() {
                    var s = this;
                    return e.prototype.initialize.apply(this, arguments), this.$element.find(".auth-block").view("Common.AuthBlock").then((function(e) {
                        s.authBlock = e, t('[data-control="Common.Auth"]').view().then((function(t) {
                            s.authPopup = t, s.authBlock.open = s.authPopup.open.bind(s.authPopup), s.authBlock.close = s.authPopup.close.bind(s.authPopup), s.authBlock.$tabs = s.authPopup.$tabs
                        }))
                    })), n.instance().getData().then((function() {
                        if (n.instance().isAuthorized()) {
                            var t = a.getArgument("url"),
                                e = null;
                            t.isSet ? e = t.value : window.location.href.indexOf("/feed/") > -1 ? e = i.redirects.feed : window.location.href.indexOf("/login/") > -1 && (e = "/"), e && (window.location.href = decodeURIComponent(e))
                        }
                    })), this
                }, s.prototype.listen = function() {
                    return e.prototype.listen.apply(this, arguments), this.$element.find(".auth__btn-remind, .auth_reg-link").on("click", function() {
                        this.authPopup.open()
                    }.bind(this)), this
                }, i.redirects = {
                    feed: "/feed/"
                }, s
            }.apply(e, a)) || (t.exports = i)
        },
        WwSU: function(t, e, n) {
            var a, i;
            a = [n("3a3M"), n("1NHe"), n("nCJl")], void 0 === (i = function(t, e, n) {
                "use strict";
                var a = {};

                function i() {
                    e.apply(this, arguments)
                }
                return i.prototype = Object.create(e.prototype), i.prototype.initialize = function() {
                    return e.prototype.initialize.apply(this, arguments), this.$input = this.$element.find(a.selectors.input), this.input = this.$input.get(0), this.timeout = 300, this.model = n.instance(), this
                }, i.prototype.listen = function() {
                    return e.prototype.listen.apply(this, arguments), this.$element.on("input paste", a.selectors.input, this.changeHandler.bind(this)).on("submit", a.selectors.form, this.changeHandler.bind(this)).on("reset", a.selectors.form, this.resetHandler.bind(this)), this
                }, i.prototype.resetHandler = function() {
                    this.model.trigger("sports:user:model:search:reset"), clearTimeout(this.timer)
                }, i.prototype.changeHandler = function(t) {
                    t.preventDefault(), clearTimeout(this.timer), this.input.value.length > 0 && this.input.value.length < 3 || (this.timer = setTimeout(this.sendRequest.bind(this), this.timeout))
                }, i.prototype.sendRequest = function() {
                    var t = this.input.value;
                    if ("" == t) return this.resetHandler();
                    t.length > 0 && t.length < 3 || (this.model.trigger("sports:user:model:search:start"), this.model.getFirstPage(t))
                }, a.selectors = {
                    input: ".js-search-input",
                    form: ".js-search-form",
                    reset: ".js-search-reset"
                }, i
            }.apply(e, a)) || (t.exports = i)
        },
        "Xx+T": function(t, e, n) {
            "use strict";
            var a, i = (a = n("x2wi")) && a.__esModule ? a : {
                default: a
            };
            t.exports = {
                "_desktop/common/views/auth/auth": i.default
            }
        },
        bpKj: function(t, e, n) {
            var a = n("Fanx");

            function i(t) {
                return t && (t.__esModule ? t.default : t)
            }
            t.exports = (a.default || a).template({
                1: function(t, e, n, a) {
                    return "Sports.ru"
                },
                3: function(t, e, a, s) {
                    var o;
                    return null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "cyber.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(4, s, 0),
                        inverse: this.program(6, s, 0),
                        data: s
                    })) ? o : ""
                },
                4: function(t, e, n, a) {
                    return "cyber.sports.ru"
                },
                6: function(t, e, n, a) {
                    return "Tribuna.com"
                },
                8: function(t, e, n, a) {
                    return "            <p>\n                Если у вас был аккаунт на Sports.ru,<br>вы можете зайти через него.\n            </p>\n"
                },
                compiler: [6, ">= 2.0.0-beta.1"],
                main: function(t, e, a, s) {
                    var o;
                    return '<div class="auth__content">\n    <form class="auth__reg">\n        <div class="auth__title">Быстрая регистрация на ' + (null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "www.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(1, s, 0),
                        inverse: this.program(3, s, 0),
                        data: s
                    })) ? o : "") + "</div>\n" + (null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "cyber.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(8, s, 0),
                        inverse: this.noop,
                        data: s
                    })) ? o : "") + '        <div class="auth__form-row">\n            <label>\n                <input class="auth__reg-input input input_size_extra-large" type="text" name="login" placeholder="Ваш e-mail">\n            </label>\n            <label class="auth__last-label">\n                <input class="auth__reg-input input input_size_extra-large" type="password" name="password" placeholder="Пароль">\n            </label>\n        </div>\n        <div class="auth__form-row">\n            <label>\n                <input class="auth__reg-input input input_size_extra-large" type="text" name="nick" placeholder="Имя на сайте">\n            </label>\n            <label class="auth__last-label">\n                <input class="auth__reg-input input input_size_extra-large" type="password" name="repasswd" placeholder="Пароль еще раз">\n            </label>\n        </div>\n        <div class="auth__form-row">\n            <label class="auth__checkbox-label">\n                <input class="auth__agreement" type="checkbox" name="agreement" checked>\n                Я принимаю <a class="link link_color_blue link_size_tiny" href="/docs/agreement/" rel="nofollow">пользовательское соглашение</a>\n            </label>\n        </div>\n        <div class="auth__form-row">\n            <button class="btn btn_color_black-light btn_size_extra-large auth__btn auth__reg-btn loader-gray data-track-click"\n            data-event-name="reg/success" data-event-category="user" data-event-value="mail" type="submit">Зарегистрироваться</button>\n\n            <div class="auth__message">\n                <span class="auth__message-error"></span>\n                <span class="auth__message-success"></span>\n            </div>\n        </div>\n    </form>\n    <p class="auth__bottom-text">\n        Через несколько секунд вы узнаете, почему ' + (null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "www.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(1, s, 0),
                        inverse: this.program(3, s, 0),
                        data: s
                    })) ? o : "") + " — самый удобный спортивный сайт\n    </p>\n</div>\n"
                },
                useData: !0
            })
        },
        go5x: function(t, e, n) {
            var a = n("Fanx");

            function i(t) {
                return t && (t.__esModule ? t.default : t)
            }
            t.exports = (a.default || a).template({
                1: function(t, e, n, a) {
                    return "<br><br>Если у вас был аккаунт на Sports.ru,<br>вы можете зайти через него."
                },
                3: function(t, e, n, a) {
                    return "Sports.ru?"
                },
                5: function(t, e, a, s) {
                    var o;
                    return null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "cyber.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(6, s, 0),
                        inverse: this.program(8, s, 0),
                        data: s
                    })) ? o : ""
                },
                6: function(t, e, n, a) {
                    return "cyber.sports.ru?"
                },
                8: function(t, e, n, a) {
                    return "Tribuna.com?"
                },
                compiler: [6, ">= 2.0.0-beta.1"],
                main: function(t, e, a, s) {
                    var o;
                    return '<div class="auth__content clearfix">\n    <form class="auth__login auth_state_error">\n        <div class="auth__title">Авторизация</div>\n        <p>\n            Войдите на сайт, чтобы оценить посты<br>\n            и комментарии.\n            ' + (null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "cyber.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(1, s, 0),
                        inverse: this.noop,
                        data: s
                    })) ? o : "") + '\n        </p>\n        <div class="auth__form-row">\n            <label>\n                <input class="auth__login-input auth__login-input_email input input_size_extra-large" type="text" name="login" placeholder="Ваш e-mail">\n            </label>\n        </div>\n        <div class="auth__form-row">\n            <label>\n                <input class="auth__login-input input input_size_extra-large" type="password" name="password" placeholder="Ваш пароль">\n            </label>\n            <a class="auth__forgot-password auth__btn-remind link link_color_blue link_size_tiny" href="#" rel="nofollow">Забыли пароль?</a>\n        </div>\n        <div class="auth__form-row">\n            <label class="auth__checkbox-label">\n                <input class="auth__remember-me" type="checkbox" name="remember_me" checked>\n                Запомнить меня\n            </label>\n        </div>\n        <div class="auth__form-row">\n            <button class="btn btn_color_black-light btn_size_extra-large auth__btn auth__login-btn loader-gray data-track-click piwikTrackContent piwikContentIgnoreInteraction"\n            data-event-name="auth/success" data-event-value="mail" type="submit" data-event-category="user">Войти</button>\n\n\n            <div class="auth__message">\n                <span class="auth__message-error"></span>\n                <span class="auth__message-success"></span>\n            </div>\n        </div>\n        <input type="hidden" name="back_url" value="/logon.html">\n    </form>\n    <p class="auth__bottom-text">\n        Еще не зарегистрированы на ' + (null != (o = i(n("/mMI")).call(t, (o = (o = s && s.root) && o.request_env) && o.HTTP_HOST, "==", "www.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(3, s, 0),
                        inverse: this.program(5, s, 0),
                        data: s
                    })) ? o : "") + '<br>\n        <a class="auth_reg-link link link_color_blue" href="#" rel="nofollow">Зарегистрироваться</a>\n    </p>\n</div>\n'
                },
                useData: !0
            })
        },
        jZI0: function(t, e, n) {},
        nCJl: function(t, e, n) {
            var a, i;
            a = [n("3a3M"), n("W6we")], void 0 === (i = function(t, e) {
                "use strict";
                var n = {};

                function a() {
                    return e.apply(this, arguments), this.limit = 5, this.page = 0, this.query = "", this
                }
                return a.prototype = Object.create(e.prototype), n.instance = null, a.instance = function() {
                    return n.instance || (n.instance = new a)
                }, a.prototype.listen = function() {
                    return e.prototype.listen.apply(this), this
                }, a.prototype.getResults = function(e) {
                    this.query = e;
                    var a = {
                        query: e = e.toLowerCase(),
                        offset: this.limit * this.page
                    };
                    return t.get(n.services.search, {
                        args: JSON.stringify(a)
                    }).then(function(t) {
                        return t.forEach((function(t) {
                            t.category = t.type, t.type = n.types[t.type] ? n.types[t.type] : t.sport_name, t.url = t.link, t.subtitle = t.description
                        })), t
                    }.bind(this), (function(t) {
                        return console.warn("[SPORTS] Error with zero-data recommendation api", t), []
                    }))
                }, a.prototype.getFirstPage = function(t) {
                    this.page = 0;
                    var e = this.getResults(t, 0);
                    return e.then(function(t) {
                        this.trigger("sports:user:model:search:update", t)
                    }.bind(this)), e
                }, a.prototype.getNextPage = function() {
                    return this.getResults(this.query, ++this.page)
                }, n.types = {
                    blog: "Блог",
                    user: "Пользователь"
                }, n.services = {
                    search: "/stat/core/search/zerodata/"
                }, a
            }.apply(e, a)) || (t.exports = i)
        },
        r6CY: function(t, e, n) {
            "use strict";
            var a = s(n("x+v/")),
                i = s(n("1NHe"));

            function s(t) {
                return t && t.__esModule ? t : {
                    default: t
                }
            }

            function o(t) {
                return (o = "function" == typeof Symbol && "symbol" == typeof Symbol.iterator ? function(t) {
                    return typeof t
                } : function(t) {
                    return t && "function" == typeof Symbol && t.constructor === Symbol && t !== Symbol.prototype ? "symbol" : typeof t
                })(t)
            }

            function r(t, e) {
                for (var n = 0; n < e.length; n++) {
                    var a = e[n];
                    a.enumerable = a.enumerable || !1, a.configurable = !0, "value" in a && (a.writable = !0), Object.defineProperty(t, a.key, a)
                }
            }

            function l(t, e) {
                return !e || "object" !== o(e) && "function" != typeof e ? function(t) {
                    if (void 0 === t) throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
                    return t
                }(t) : e
            }

            function c(t) {
                return (c = Object.setPrototypeOf ? Object.getPrototypeOf : function(t) {
                    return t.__proto__ || Object.getPrototypeOf(t)
                })(t)
            }

            function u(t, e) {
                return (u = Object.setPrototypeOf || function(t, e) {
                    return t.__proto__ = e, t
                })(t, e)
            }
            var p = s(n("4mDg")).default.instance(),
                h = {},
                d = function(t) {
                    function e() {
                        var t;
                        ! function(t, e) {
                            if (!(t instanceof e)) throw new TypeError("Cannot call a class as a function")
                        }(this, e);
                        for (var n = arguments.length, a = new Array(n), i = 0; i < n; i++) a[i] = arguments[i];
                        return l(this, (t = c(e)).call.apply(t, [this].concat(a)))
                    }
                    var n, s, o;
                    return function(t, e) {
                        if ("function" != typeof e && null !== e) throw new TypeError("Super expression must either be null or a function");
                        t.prototype = Object.create(e && e.prototype, {
                            constructor: {
                                value: t,
                                writable: !0,
                                configurable: !0
                            }
                        }), e && u(t, e)
                    }(e, t), n = e, (s = [{
                        key: "initialize",
                        value: function() {
                            return i.default.prototype.initialize.apply(this, arguments), this.modal = new a.default(this.$element[0], "Common.Modal").initialize().listen(), this.$popup = this.$element.find(h.selectors.popup), this.timer = null, this
                        }
                    }, {
                        key: "listen",
                        value: function() {
                            return i.default.prototype.listen.apply(this, arguments), this.modal.on("opened", h.open.bind(this)), this.modal.on("closed", h.close.bind(this)), p.on("ui:feedback:show", this.open.bind(this)), p.on("ui:feedback:hide", this.close.bind(this)), this
                        }
                    }, {
                        key: "open",
                        value: function(t, e) {
                            e && (this.timer = setTimeout(this.close.bind(this), e)), this.modal.open(), h.open.call(this, t), p.trigger("ui:feedback:opened")
                        }
                    }, {
                        key: "close",
                        value: function() {
                            this.timer && (clearTimeout(this.timer), this.timer = null), this.modal.close(), h.close.call(this), p.trigger("ui:feedback:closed")
                        }
                    }]) && r(n.prototype, s), o && r(n, o), e
                }(i.default);
            h.open = function(t) {
                this.$popup.html(t), this.$element.addClass(h.modifiers.open), this.$element.removeClass(h.modifiers.closed)
            }, h.close = function() {
                this.$element.addClass(h.modifiers.closed), this.$element.removeClass(h.modifiers.open)
            }, h.selectors = {
                popup: ".popup"
            }, h.modifiers = {
                open: "is-open",
                closed: "is-closed"
            }, t.exports = d
        },
        "x+v/": function(t, e, n) {
            var a, i;
            a = [n("3a3M"), n("1NHe")], void 0 === (i = function(t, e) {
                "use strict";
                var n = {};

                function a() {
                    e.apply(this, arguments)
                }
                return a.prototype = Object.create(e.prototype), a.prototype.constructor = a, a.prototype.initialize = function() {
                    return e.prototype.initialize.apply(this, arguments), this.state = "closed", this.scrollWidth = null, this.$body = t("body"), this.$userPanel = this.$body.children(n.selectors.userPanel), this.keyDownHandlerLink = this.keyDownHandler.bind(this), this
                }, a.prototype.listen = function() {
                    return e.prototype.listen.apply(this, arguments), this.$element.on("click", n.selectors.close, this.close.bind(this)).on("click", this.backDropClick.bind(this)), this
                }, a.prototype.open = function() {
                    return "closed" === this.state && (null === this.scrollWidth && (this.scrollWidth = n.get_scroll_bar_width()), this.state = "opened", this.$body.on("keydown", this.keyDownHandlerLink), this.$body.addClass(n.modifiers.open).css("margin-right", this.scrollWidth), this.$userPanel.css("margin-left", -1 * this.scrollWidth / 2 + "px"), this.trigger("opened")), this
                }, a.prototype.close = function(t) {
                    return t && t.preventDefault(), "opened" === this.state && (this.state = "closed", this.$body.off("keydown", this.keyDownHandlerLink), this.$body.removeClass(n.modifiers.open).css("margin-right", 0), this.$userPanel.css("margin-left", 0), this.trigger("closed")), this
                }, a.prototype.backDropClick = function(t) {
                    return 2 === t.eventPhase && this.close(t), this
                }, a.prototype.keyDownHandler = function(t) {
                    switch (t.keyCode) {
                        case 27:
                            this.close(t)
                    }
                    return this
                }, a.prototype.attributes = {
                    delayed: !0
                }, n.get_scroll_bar_width = function() {
                    var t, e, n, a = document.createElement("div");
                    return a.style.visibility = "hidden", a.style.width = "100px", a.style.msOverflowStyle = "scrollbar", document.body.appendChild(a), e = a.offsetWidth, a.style.overflow = "scroll", (n = document.createElement("div")).style.width = "100%", a.appendChild(n), t = n.offsetWidth, a.parentNode.removeChild(a), e - t
                }, n.selectors = {
                    userPanel: ".user-panel",
                    close: ".popup__close"
                }, n.modifiers = {
                    open: "modal_state_open"
                }, a
            }.apply(e, a)) || (t.exports = i)
        },
        x2wi: function(t, e, n) {
            var a = n("Fanx");
            t.exports = (a.default || a).template({
                1: function(t, e, n, a) {
                    return '                    <a class="auth__social-btn btn btn_size_extra-large btn-social btn-social-yandex btn_expand btn_display_block js-active data-track-click" rel="nofollow" data-control="Common.Link" data-event-category="user" data-action="yandex" href="#" data-event-label="user-panel" data-event-name="auth/success" data-event-value="yandex" data-redirect="/feed/start/">\n                        <svg class="svg-icon icon-gg" width="40" height="40">\n                            <use xlink:href="#ya"></use>\n                        </svg>\n                        Яндекс\n                    </a>\n'
                },
                3: function(t, e, n, a) {
                    return '                    data-control="Common.NewTabs"\n'
                },
                5: function(t, e, n, a) {
                    return '                    data-control="Common.Tabs"\n'
                },
                compiler: [6, ">= 2.0.0-beta.1"],
                main: function(t, e, a, i) {
                    var s, o;
                    return '\x3c!--[if lt IE 9]><div class="popup__overlay popup__overlay_ie"></div><![endif]--\x3e\n<div class="popup__overlay js-active" data-control="Common.Auth">\n    <div class="popup auth clearfix">\n        <a class="popup__close" href="#" title="Закрыть" rel="nofollow"><i class="icon-close"></i></a>\n        <div class="auth__side">\n            Войти как пользователь:\n            <div class="auth__social-btn-wrap">\n                <a class="auth__social-btn btn btn_size_extra-large btn-social btn-social-vk btn_expand btn_display_block js-active data-track-click" rel="nofollow" data-control="Common.Link" data-event-category="user" data-action="vk-login" href="#" data-event-label="user-panel" data-event-name="auth/success" data-event-value="vk">\n                    <svg class="svg-icon" width="26" height="23">\n                        <use xlink:href="#vk"></use>\n                    </svg>\n                    ВКонтакте\n                </a>\n                <a class="auth__social-btn btn btn_size_extra-large btn-social btn-social-fb btn_expand btn_display_block js-active data-track-click" rel="nofollow" data-control="Common.Link" data-event-category="user" data-action="fb-login" href="#" data-event-label="user-panel" data-event-name="auth/success" data-event-value="fb">\n                    <svg class="svg-icon" width="26" height="23">\n                        <use xlink:href="#fb-simple"></use>\n                    </svg>\n                    Facebook\n                </a>\n                <a class="auth__social-btn btn btn_size_extra-large btn-social btn-social-gg btn_expand btn_display_block js-active data-track-click" rel="nofollow" data-control="Common.Link" data-event-category="user" data-action="gg-login" href="#" data-event-label="user-panel" data-event-name="auth/success" data-event-value="g+">\n                    <svg class="svg-icon icon-gg" width="40" height="40">\n                        <use xlink:href="#google-mobile-2"></use>\n                    </svg>\n                    Google\n                </a>\n' + (null != (s = (o = n("/mMI"), o && (o.__esModule ? o.default : o)).call(t, null != (s = null != t ? t.request_env : t) ? s.HTTP_HOST : s, "==", "www.sports.ru", {
                        name: "ifCond",
                        hash: {},
                        fn: this.program(1, i, 0),
                        inverse: this.noop,
                        data: i
                    })) ? s : "") + '            </div>\n        </div>\n        <div class="auth__main">\n            <div class="js-captcha-container"></div>\n            <div class="tabs tabs_state_horizontal auth__tabs js-active"\n                 data-animate="horizontal-slide"\n' + (null != (s = e.if.call(t, null != t ? t.is_old_static : t, {
                        name: "if",
                        hash: {},
                        fn: this.program(3, i, 0),
                        inverse: this.program(5, i, 0),
                        data: i
                    })) ? s : "") + '                >\n\n                <div class="tabs__body">\n\n                    <div class="tabs__panel" role="tabpanel">\n\n' + (null != (s = this.invokePartial(n("go5x"), t, {
                        name: "_desktop/common/views/auth/authorization",
                        data: i,
                        indent: "                        ",
                        helpers: e,
                        partials: a
                    })) ? s : "") + '\n                    </div>\n\n                    <div class="tabs__panel" role="tabpanel">\n\n' + (null != (s = this.invokePartial(n("bpKj"), t, {
                        name: "_desktop/common/views/auth/registration",
                        data: i,
                        indent: "                        ",
                        helpers: e,
                        partials: a
                    })) ? s : "") + '\n                    </div>\n\n                    <div class="tabs__panel" role="tabpanel">\n\n' + (null != (s = this.invokePartial(n("G8mn"), t, {
                        name: "_desktop/common/views/auth/remind",
                        data: i,
                        indent: "                        ",
                        helpers: e,
                        partials: a
                    })) ? s : "") + '\n                    </div>\n\n                </div>\n\n            </div>\n\n\n\n\n        </div>\n    </div>\n    \x3c!--[if lt IE 9]><div class="popup__v-align_fix"></div><![endif]--\x3e\n</div>\n'
                },
                usePartial: !0,
                useData: !0
            })
        },
        yfTL: function(t, e, n) {
            "use strict";
            var a = n("egl0");
            a.Loader.control("Common.Feedback", n("JgMM")), a.Loader.control("Common.AuthBlock", n("5yIE")), a.Loader.control("User.Search", n("WwSU")), a.Loader.control("User.Login", n("Ogd4")), a.Loader.control("Banners.Direct", n("CY+l")), a.Loader.control("Banners.DFP", n("s72K")), (0, a.Bootstrap)()
        }
    },
    [
        ["yfTL", 0, 1]
    ]
]);