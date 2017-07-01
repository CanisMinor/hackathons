library(shiny)
library(timevis)
library(leaflet)
library(plotly)
library(igraph)
library(lubridate)


# create colours for map
r_colors <- rgb(t(col2rgb(colors()) / 255))
names(r_colors) <- colors()

# set working directory
setwd("/home/cecilia/Documents/hackathons/viz/src")

# read in data
tags = read.csv("../data/test_data.txt")
names = read.csv("../data/names.txt")
states = read.csv("../data/states.txt")
data_cleaned = read.csv2(file="../../refined_data/clean_data.csv", sep=",", dec=".", header=FALSE, colClasses=c(NA, NA, NA, NA, NA, "Date"))

data <- data.frame(
  id      = 1:300,
  content = c("Item one", "Item two",
              "Ranged item", "Item four"),
  start   = c("2016-01-10", "2016-01-11",
              "2016-01-20", "2016-02-14 15:00:00"),
  end     = c(NA, NA, NA, NA)
)

data_dates <- data.frame(
  id      = 1:300,
  content = data_cleaned$V1,
  start   = data_cleaned$V5,
  end     = c(rep(NA, 300))
)

# Create fake data
src <- c("Reynolds", "Reynolds", "Reynolds", "Reynolds", "Porter", "Porter", "Chamberlain", "Chamberlain", "LeCun")
target <- c("Porter", "Chamberlain", "Whittle", "Hinton", "Ericsson", "Fairman", "George", "Reynolds", "Ising")
networkData <- data.frame(src, target)


ui <- fluidPage(
    
    #titlePanel("eJuris"),

      mainPanel(
        tabsetPanel(
          tabPanel("Dates", timevisOutput("timeline")),
          tabPanel("Places", leafletOutput("mymap"), p()),
          tabPanel("People", simpleNetwork(networkData, zoom=TRUE))
        )
      )
)

server <- function(input, output, session) {
  output$timeline <- renderTimevis({
    timevis(data_dates, fit=TRUE)
  })
  
  #points <- eventReactive(input$recalc, {
  #  cbind(rnorm(40) * 2 + 13, rnorm(40) + 48)
  #}, ignoreNULL = FALSE)
  
  points <- eventReactive(input$recalc, {
      cbind(-data_cleaned$V4, data_cleaned$V3)
    }, ignoreNULL = FALSE)
    
  output$mymap <- renderLeaflet({leaflet() %>%
      addProviderTiles(providers$Stamen.TonerLite,
                       options = providerTileOptions(noWrap = TRUE)
      ) %>%
      addMarkers(data = points())
  })
}

shinyApp(ui = ui, server = server)

