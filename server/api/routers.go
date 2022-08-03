package api

import (
	"github.com/gin-gonic/gin"
	ctx "gitlab.eng.vmware.com/opensource/tracecruncher-api/internal/tracerctx"
)

var (
	apiVersion = "v1"
)

// map request path to logic
func NewRouter(t *ctx.Tracer) *gin.Engine {
	router := gin.Default()
	router.GET("/"+apiVersion+"/traces", t.SystemCallGet)
	router.GET("/"+apiVersion+"/traces/:id", t.SystemCallStatus)
	router.POST("/"+apiVersion+"/traces", t.SystemCallPost)
	router.DELETE("/"+apiVersion+"/traces/:id", t.SystemCallDelete)
	router.GET("/"+apiVersion+"/pods", t.LocalPodsGet)
	router.GET("/"+apiVersion+"/trace-hooks", t.TraceHooksGet)
	return router
}
