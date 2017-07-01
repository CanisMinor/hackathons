library(shiny)
library(timevis)
library(leaflet)
library(plotly)
library(igraph)


# create colours for map
r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()


# set working directory
setwd("/home/cecilia/Documents/hackathons/viz/src")

# read in data
tags = read.csv("../data/test_data.txt")
names = read.csv("../data/names.txt")
states = read.csv("../data/states.txt")

data <- data.frame(
  id      = 1:4,
  content = c("Item one", "Item two",
              "Ranged item", "Item four"),
  start   = c("2016-01-10", "2016-01-11",
              "2016-01-20", "2016-02-14 15:00:00"),
  end     = c(NA, NA, "2016-02-04", NA)
)

ui <- fluidPage(
    
    titlePanel("eJuries"),
    
    sidebarLayout(
      
      sidebarPanel(
        # Inputs excluded for brevity
      ),
      
      mainPanel(
        tabsetPanel(
          tabPanel("Dates", timevisOutput("timeline")), 
          tabPanel("Places", leafletOutput("mymap"),
                   p(),
                   actionButton("recalc", "New points")), 
          tabPanel("People", chart_link)
        )
      )
    )
)

server <- function(input, output, session) {
  output$timeline <- renderTimevis({
    timevis(data)
  })
  
  points <- eventReactive(input$recalc, {
    cbind(rnorm(40) * 2 + 13, rnorm(40) + 48)
  }, ignoreNULL = FALSE)
  
  output$mymap <- renderLeaflet({
    leaflet() %>%
      addProviderTiles(providers$Stamen.TonerLite,
                       options = providerTileOptions(noWrap = TRUE)
      ) %>%
      addMarkers(data = points())
  })
}

shinyApp(ui = ui, server = server)
