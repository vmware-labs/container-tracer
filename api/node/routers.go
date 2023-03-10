// SPDX-License-Identifier: GPL-2.0-or-later
/*
 * Copyright (C) 2022 VMware, Inc. Enyinna Ochulor (VMware) <enyinnaochulor@gmail.com>
 * Copyright (C) 2022 VMware, Inc. Tzvetomir Stoyanov (VMware) <tz.stoyanov@gmail.com>
 *
 * Tracer REST API.
 */
package api

import (
	"github.com/gin-gonic/gin"
	"github.com/vmware-labs/container-tracer/api"
	ctx "github.com/vmware-labs/container-tracer/internal/tracerctx"
)

var (
	apiVersion = "v1"
)

// map request path to logic
func NewRouter(t *ctx.Tracer) *gin.Engine {
	router := api.Router.SetupRouter()
	router.GET("/"+apiVersion+"/pods", t.LocalPodsGet)
	router.GET("/"+apiVersion+"/trace-hooks", t.TraceHooksGet)
	router.POST("/"+apiVersion+"/trace-session", t.TraceSessionPost)
	router.GET("/"+apiVersion+"/trace-session/:id", t.TraceSessionGet)
	router.PUT("/"+apiVersion+"/trace-session/:id", t.TraceSessionPut)
	router.DELETE("/"+apiVersion+"/trace-session/:id", t.TraceSessionDel)
	return router
}
